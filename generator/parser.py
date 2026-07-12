"""
parser.py — Varre os repositórios de system prompts e constrói um índice estruturado.
Extrai: modelo, empresa, data, tamanho em tokens, tags XML, tools mencionados.
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Caminho para o archive com os 20 repos
ARCHIVE_PATH = Path("/workspace/leaked-prompts-archive")

# Empresas reconhecidas pelo path
COMPANY_PATTERNS = {
    "Anthropic": ["Anthropic", "anthropic"],
    "OpenAI": ["OpenAI", "openai", "ChatGPT", "codex", "Codex"],
    "Google": ["Google", "google", "Gemini", "gemini", "Jules", "NotebookLM"],
    "xAI": ["xAI", "xai", "Grok", "grok"],
    "Perplexity": ["Perplexity", "perplexity"],
    "Microsoft": ["Microsoft", "microsoft", "Copilot", "copilot"],
    "Meta": ["Meta", "meta", "Llama", "llama"],
    "Mistral": ["Mistral", "mistral", "Mixtral"],
    "DeepSeek": ["DeepSeek", "deepseek"],
    "Alibaba": ["Alibaba", "Qwen", "qwen", "Tongyi"],
    "Moonshot": ["Moonshot", "Kimi", "kimi"],
    "Zhipu": ["Zhipu", "GLM", "Z.AI", "z.ai"],
    "Cursor": ["Cursor", "cursor"],
    "Devin": ["Devin", "devin"],
    "Replit": ["Replit", "replit"],
    "Windsurf": ["Windsurf", "windsurf"],
    "Manus": ["Manus", "manus"],
    "Lovable": ["Lovable", "lovable"],
    "Notion": ["Notion", "notion"],
    "Brave": ["Brave", "brave"],
    "Discord": ["Discord", "discord", "Clyde"],
    "Other": [],
}

# Detecta modelo a partir do nome do arquivo
MODEL_PATTERNS = [
    (r"claude[- ]?(fable|mythos|opus|sonnet|haiku)[\s-]*(\d+(\.\d+)*)", "claude"),
    (r"gpt[- ]?(\d+(\.\d+)*)(\s+(thinking|instant|codex))?", "gpt"),
    (r"gemini[\s-]*(\d+(\.\d+)*)\s*(pro|flash|ultra)?", "gemini"),
    (r"grok[\s-]*(\d+(\.\d+)*)", "grok"),
    (r"o(\d+)(-mini|-pro)?", "o-series"),
    (r"deepseek[\s-]*(v?\d+(\.\d+)*)?\s*(r\d+)?", "deepseek"),
    (r"qwen[\s-]*(\d+(\.\d+)*)?", "qwen"),
    (r"kimi[\s-]*(k\d+(\.\d+)*)?", "kimi"),
    (r"glm[\s-]*(\d+(\.\d+)*)?", "glm"),
    (r"mistral[\s-]*(\w+)?", "mistral"),
    (r"llama[\s-]*(\d+(\.\d+)*)?", "llama"),
    (r"mixtral[\s-]*(\w+)?", "mixtral"),
    (r"command[\s-]*(\w+)?", "cohere"),
]

# Detecta data a partir do nome do arquivo
DATE_PATTERN = re.compile(r"(\d{4})[\-_](\d{1,2})[\-_](\d{1,2})|(\d{1,2})[\-_](\d{1,2})[\-_](\d{4})")

# Tags XML comumente usadas em system prompts
XML_TAGS = re.compile(r"<(\w[\w\-]*)>")

# Indica tools mencionados
TOOL_PATTERNS = [
    r"\b(bash|terminal|shell)\b",
    r"\b(search|web_search|fetch)\b",
    r"\b(file_read|file_write|read_file|write_file)\b",
    r"\b(memory|recall|remember)\b",
    r"\b(calculator|math)\b",
    r"\b(image_gen|image_generation|generate_image)\b",
    r"\b(code_execution|code_exec|interpreter)\b",
    r"\b(browser|navigate|click)\b",
    r"\b(database|sql)\b",
    r"\b(calendar|email|contact)\b",
    r"\b(mcp|MCP)\b",
]


def detect_company(path_str: str) -> str:
    """Detecta empresa pelo path do arquivo."""
    for company, patterns in COMPANY_PATTERNS.items():
        if company == "Other":
            continue
        for p in patterns:
            if p in path_str:
                return company
    return "Other"


def detect_model(filename: str, content: str = "") -> str:
    """Detecta o modelo a partir do nome do arquivo ou conteúdo."""
    text = filename.lower()
    # Tenta do filename primeiro
    for pattern, prefix in MODEL_PATTERNS:
        m = re.search(pattern, text)
        if m:
            return m.group(0).replace(" ", "-")
    # Tenta do conteúdo (primeiras 200 chars)
    if content:
        head = content[:500].lower()
        for pattern, prefix in MODEL_PATTERNS:
            m = re.search(pattern, head)
            if m:
                return m.group(0).replace(" ", "-")
    return "unknown"


def detect_date(filename: str) -> str:
    """Extrai data do nome do arquivo."""
    m = DATE_PATTERN.search(filename)
    if m:
        groups = [g for g in m.groups() if g]
        if len(groups) == 3:
            # Tenta yyyy-mm-dd primeiro, depois mm-dd-yyyy
            if len(groups[0]) == 4:
                return f"{groups[0]}-{int(groups[1]):02d}-{int(groups[2]):02d}"
            else:
                return f"{groups[2]}-{int(groups[0]):02d}-{int(groups[1]):02d}"
    return ""


def estimate_tokens(text: str) -> int:
    """Estimativa grosseira: ~4 chars por token."""
    return len(text) // 4


def extract_xml_tags(content: str) -> list:
    """Extrai tags XML únicas usadas."""
    return sorted(set(XML_TAGS.findall(content)))


def detect_tools(content: str) -> list:
    """Detecta tools mencionados no prompt."""
    found = []
    lower = content.lower()
    for p in TOOL_PATTERNS:
        if re.search(p, lower):
            tool_name = p.replace(r"\b", "").replace("\\", "")
            found.append(tool_name)
    return found


def extract_persona(content: str) -> str:
    """Tenta extrair a primeira frase que define a persona."""
    # Procura "You are..." ou "Você é..."
    patterns = [
        r"You are\s+([^\.\n]{10,150})",
        r"Você é\s+([^\.\n]{10,150})",
        r"I am\s+([^\.\n]{10,150})",
    ]
    for p in patterns:
        m = re.search(p, content)
        if m:
            return m.group(1).strip()[:150]
    return ""


def parse_file(filepath: Path) -> dict:
    """Analisa um arquivo de system prompt."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None
    if len(content) < 100:
        return None  # Pula arquivos muito pequenos (não são prompts reais)
    rel_path = str(filepath.relative_to(ARCHIVE_PATH))
    return {
        "id": rel_path.replace("/", "__").replace(".", "_")[:200],
        "path": rel_path,
        "filename": filepath.name,
        "company": detect_company(rel_path),
        "model": detect_model(filepath.name, content),
        "date": detect_date(filepath.name),
        "size_bytes": filepath.stat().st_size,
        "tokens_estimate": estimate_tokens(content),
        "lines": content.count("\n") + 1,
        "xml_tags": extract_xml_tags(content),
        "tools": detect_tools(content),
        "persona": extract_persona(content),
        "has_examples": "Example" in content or "example" in content or "EXAMPLE" in content,
        "has_tools_section": "tools" in content.lower()[:5000],
        "has_memory_section": "memory" in content.lower()[:10000],
        "preview": content[:400].strip(),
    }


def scan_all_repos() -> list:
    """Varre todos os repos e retorna lista de prompts indexados."""
    results = []
    for filepath in ARCHIVE_PATH.rglob("*"):
        if not filepath.is_file():
            continue
        # Só processa arquivos de texto razoáveis
        if filepath.suffix.lower() not in (".md", ".txt", ".mkd", ".markdown", ".json", ".yaml", ".yml"):
            continue
        if filepath.stat().st_size > 500_000:  # > 500KB pula
            continue
        info = parse_file(filepath)
        if info:
            results.append(info)
    return results


if __name__ == "__main__":
    print("Varrendo repositórios...")
    prompts = scan_all_repos()
    print(f"Encontrados: {len(prompts)} prompts")
    # Stats
    by_company = defaultdict(int)
    for p in prompts:
        by_company[p["company"]] += 1
    print("\nPor empresa:")
    for c, n in sorted(by_company.items(), key=lambda x: -x[1]):
        print(f"  {c}: {n}")
    # Salva índice
    out = Path("/workspace/meta-prompt-engine/data/index.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(prompts, indent=2, ensure_ascii=False))
    print(f"\nÍndice salvo em {out}")
    print(f"Tamanho: {out.stat().st_size / 1024:.1f} KB")
