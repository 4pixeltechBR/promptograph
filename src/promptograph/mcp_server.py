"""promptograph.mcp_server — Servidor FastMCP nativo para o Promptograph.

Expõe 7 ferramentas completas via MCP (Model Context Protocol):
  1. promptograph_search(query, company?, model?, limit?)
  2. promptograph_validate(content)
  3. promptograph_generate(preset_name?, spec_json?)
  4. promptograph_stats()
  5. promptograph_skills_search(query, category?, limit?)
  6. promptograph_skills_get(skill_id)
  7. promptograph_skills_categories()

Compatível com Claude Desktop, Claude Code, Cursor, Windsurf, Antigravity e agentes autônomos.
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any

try:
    from mcp.server.fastmcp import FastMCP
except (ImportError, ModuleNotFoundError):
    try:
        from fastmcp import FastMCP
    except (ImportError, ModuleNotFoundError):
        from mcp.server.mcpserver import MCPServer as FastMCP

from promptograph import (
    build_prompt,
    validate_prompt,
    PRESET_TEMPLATES,
    search_skills,
    get_skill_blueprint,
    get_skills_stats,
)

log = logging.getLogger("4pixeltech.promptograph.mcp")
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)

_PKG_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _PKG_DIR.parent.parent

_INDEX_PATHS = [
    _PKG_DIR / "data" / "index_filtered.json",
    _REPO_ROOT / "data" / "index_filtered.json",
    _REPO_ROOT / "data" / "promptograph" / "index_filtered.json",
]


def _infer_company(path: str, repo: str = "") -> str:
    p_up = path.upper()
    if "ANTHROPIC" in p_up or "CLAUDE" in p_up:
        return "Anthropic"
    if "OPENAI" in p_up or "GPT" in p_up or "CHATGPT" in p_up:
        return "OpenAI"
    if "GOOGLE" in p_up or "GEMINI" in p_up:
        return "Google"
    if "XAI" in p_up or "GROK" in p_up:
        return "xAI"
    if "DEEPSEEK" in p_up:
        return "DeepSeek"
    if "META" in p_up or "LLAMA" in p_up or "MUSE" in p_up:
        return "Meta"
    if "CURSOR" in p_up:
        return "Cursor"
    if "MISTRAL" in p_up:
        return "Mistral"
    if "PERPLEXITY" in p_up:
        return "Perplexity"
    if "COGNITION" in p_up or "DEVIN" in p_up:
        return "Cognition"
    if "WINDSURF" in p_up:
        return "Windsurf"
    if "ZHIPU" in p_up or "GLM" in p_up or "ZCODE" in p_up:
        return "Zhipu AI"
    if "MOONSHOT" in p_up or "KIMI" in p_up:
        return "Moonshot AI"
    return repo.strip("/") if repo and repo != "/" else "Community"


def _load_prompts_index() -> list[dict[str, Any]]:
    for path in _INDEX_PATHS:
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                raw_entries = data.get("entries", []) if isinstance(data, dict) else data
                log.info(f"[promptograph-mcp] Carregando {len(raw_entries)} prompts de {path}")

                unified = []
                for p in raw_entries:
                    p_path = p.get("path", "")
                    filename = Path(p_path).name
                    company = p.get("company") or _infer_company(p_path, p.get("repo", ""))
                    model = p.get("model") or p.get("title") or filename.rsplit(".", 1)[0]
                    tokens = p.get("tokens") or (p.get("words", 0) * 4 // 3) or (p.get("size_bytes", 0) // 4)

                    unified.append({
                        "id": p.get("id") or p_path.replace("/", "__").replace("\\", "__"),
                        "filename": filename,
                        "company": company,
                        "model": model,
                        "tokens": tokens,
                        "persona": p.get("persona", "")[:120],
                        "preview": p.get("preview", "")[:250],
                        "path": p_path,
                    })

                log.info(f"[promptograph-mcp] Total indexado e operacional: {len(unified)} prompts")
                return unified
            except Exception as e:
                log.error(f"[promptograph-mcp] Falha ao ler {path}: {e}")

    log.warning("[promptograph-mcp] Nenhum índice de prompts encontrado.")
    return []


_INDEX: list[dict[str, Any]] = _load_prompts_index()

mcp = FastMCP("promptograph")


@mcp.tool()
def promptograph_search(query: str, company: str = "", model: str = "", limit: int = 20) -> str:
    """Busca prompts indexados no catálogo oficial de 20.475 prompts de produção.

    Args:
        query: Texto para buscar (no filename, path, persona, model ou preview).
        company: Filtra por empresa (Anthropic, OpenAI, Google, xAI, Meta, DeepSeek, Cursor, etc).
        model: Filtra por modelo (ex: claude, gpt, gemini, grok, glm, kimi).
        limit: Máximo de resultados (default 20, max 100).

    Returns:
        JSON com total encontrado e lista resumida de prompts.
    """
    limit = max(1, min(int(limit), 100))
    q_lower = query.lower().strip()
    c_lower = company.lower().strip()
    m_lower = model.lower().strip()
    results = []

    for p in _INDEX:
        if c_lower and c_lower not in p.get("company", "").lower():
            continue
        if m_lower and m_lower not in p.get("model", "").lower() and m_lower not in p.get("filename", "").lower():
            continue

        if q_lower:
            text = f"{p.get('filename','')} {p.get('path','')} {p.get('persona','')} {p.get('model','')} {p.get('preview','')}".lower()
            if q_lower not in text:
                continue

        results.append(p)
        if len(results) >= limit:
            break

    return json.dumps({
        "total_hits": len(results),
        "query": query,
        "company": company or "all",
        "model": model or "all",
        "results": results,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def promptograph_validate(content: str) -> str:
    """Valida um system prompt contra 13 boas práticas e 6 red flags de produção.

    Args:
        content: Conteúdo integral do system prompt para auditar.

    Returns:
        JSON estruturado com score (0-100%), nota (A+ a F), regras aprovadas, falhas e avisos.
    """
    result = validate_prompt(content)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def promptograph_generate(preset_name: str = "claude_coding_agent", spec_json: str = "") -> str:
    """Gera um system prompt de nível de produção a partir de presets ou especificação JSON.

    Args:
        preset_name: Nome do preset (claude_coding_agent, gpt5_assistant, cursor_style_coding, perplexity_search, devin_autonomous).
        spec_json: (Opcional) JSON com campos customizados para sobrescrever no preset.

    Returns:
        Prompt gerado em markdown estruturado com tags XML e regras de produção.
    """
    if preset_name not in PRESET_TEMPLATES:
        available = list(PRESET_TEMPLATES.keys())
        return json.dumps({
            "error": f"Preset '{preset_name}' não encontrado.",
            "available_presets": available,
        }, ensure_ascii=False)

    spec = PRESET_TEMPLATES[preset_name]["spec"].copy()
    if spec_json:
        try:
            custom = json.loads(spec_json)
            spec.update(custom)
        except Exception as e:
            return json.dumps({"error": f"JSON inválido em spec_json: {e}"})

    prompt_text = build_prompt(spec)
    validation = validate_prompt(prompt_text)

    return json.dumps({
        "preset": preset_name,
        "score": validation["score"],
        "grade": validation["grade"],
        "tokens_estimate": validation["stats"]["tokens_estimate"],
        "prompt": prompt_text,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def promptograph_stats() -> str:
    """Retorna estatísticas completas do corpus indexado pelo Promptograph.

    Returns:
        JSON com total de prompts (20.475), tokens estimados, contagem por empresa e modelos.
    """
    from collections import Counter
    companies = Counter(p.get("company", "Other") for p in _INDEX)
    models = Counter(p.get("model", "unknown") for p in _INDEX)
    total_tokens = sum(p.get("tokens", 0) for p in _INDEX)

    return json.dumps({
        "total_prompts": len(_INDEX),
        "total_tokens_estimate": total_tokens,
        "top_companies": dict(companies.most_common(12)),
        "top_models": dict(models.most_common(12)),
        "presets_count": len(PRESET_TEMPLATES),
        "version": "0.3.1",
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def promptograph_skills_search(query: str = "", category: str = "", limit: int = 20) -> str:
    """Busca no catálogo operacional de 226+ skills curadas de engenharia e IA.

    Args:
        query: Termo de busca (ex: 'clean-code', 'audio', 'agent', 'video').
        category: Filtro por categoria (ex: '19_Engenharia_de_Software_de_Elite').
        limit: Quantidade máxima de resultados (1-100).

    Returns:
        JSON com as skills encontradas contendo ID, nome, categoria, descrição e tags.
    """
    skills = search_skills(query=query, category=category, limit=limit)
    return json.dumps({
        "total_found": len(skills),
        "query": query,
        "category": category or "all",
        "skills": skills,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def promptograph_skills_get(skill_id: str) -> str:
    """Recupera os detalhes completos e o blueprint executável (SKILL.md) de uma skill.

    Args:
        skill_id: Identificador da skill (ex: 'clean-code', 'hectorg-jarvis-voice-desktop-agent').

    Returns:
        JSON contendo o blueprint markdown operacional da skill.
    """
    skill = get_skill_blueprint(skill_id)
    if not skill:
        return json.dumps({
            "error": f"Skill '{skill_id}' não encontrada.",
            "hint": "Use promptograph_skills_search para listar os IDs válidos.",
        }, ensure_ascii=False)

    return json.dumps(skill, ensure_ascii=False, indent=2)


@mcp.tool()
def promptograph_skills_categories() -> str:
    """Lista todas as 37 categorias do arsenal de skills e a contagem por categoria.

    Returns:
        JSON com total de skills, total de categorias e breakdown detalhado.
    """
    stats = get_skills_stats()
    return json.dumps(stats, ensure_ascii=False, indent=2)


def main() -> None:
    """Ponto de entrada do servidor FastMCP."""
    mcp.run()


if __name__ == "__main__":
    main()
