"""scripts/promptograph_mcp_server.py — MCP server stdio para o Promptograph.

Expõe ferramentas completas via MCP (Model Context Protocol):
  1. Engenharia de Prompts (20.475 prompts reais de 55 repositórios):
     - promptograph_search(query, company?, model?, limit?) -> busca prompts indexados
     - promptograph_validate(content) -> pontua 0-100%, nota A+ a F (13 regras)
     - promptograph_generate(preset_name?, spec_json?) -> gera prompt de preset ou custom
     - promptograph_stats() -> estatísticas completas do corpus (20.475 prompts)
  2. Arsenal de Skills Curadas (226+ skills em 37 categorias):
     - promptograph_skills_search(query, category?, limit?) -> busca skills curadas
     - promptograph_skills_get(skill_id) -> obtém o blueprint operacional da skill
     - promptograph_skills_categories() -> lista categorias e contagem de skills

Usa FastMCP para simplicidade. Roda via stdio transport (compatível com Claude Desktop,
Claude Code, Cursor, Windsurf, Antigravity e agentes autônomos).

Organização: 4pixeltechBR
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any

# Path setup — adiciona raiz do repo ao sys.path
_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

from mcp.server.fastmcp import FastMCP

from src.skills.promptograph import (
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

# ── Carrega e unifica índice de prompts (20.475 prompts) ────────────────

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
    # 1. Carrega metadados ricos existentes se disponíveis
    rich_map: dict[str, dict] = {}
    rich_path = _ROOT / "data" / "promptograph" / "index_filtered.json"
    if rich_path.exists():
        try:
            items = json.loads(rich_path.read_text(encoding="utf-8"))
            if isinstance(items, list):
                for item in items:
                    key = item.get("path") or item.get("filename")
                    if key:
                        rich_map[key] = item
        except Exception as e:
            log.warning(f"Erro ao ler rich index: {e}")

    # 2. Carrega índice principal de 20.475 prompts
    main_path = _ROOT / "data" / "index_filtered.json"
    unified: list[dict[str, Any]] = []

    if main_path.exists():
        try:
            data = json.loads(main_path.read_text(encoding="utf-8"))
            raw_entries = data.get("entries", []) if isinstance(data, dict) else data
            log.info(f"[promptograph-mcp] Carregando {len(raw_entries)} prompts de {main_path}")

            for p in raw_entries:
                path = p.get("path", "")
                filename = Path(path).name
                rich = rich_map.get(path) or rich_map.get(filename) or {}

                company = rich.get("company") or _infer_company(path, p.get("repo", ""))
                model = rich.get("model") or p.get("title") or filename.rsplit(".", 1)[0]
                tokens = rich.get("tokens_estimate") or (p.get("words", 0) * 4 // 3) or (p.get("size_bytes", 0) // 4)

                unified.append({
                    "id": rich.get("id") or path.replace("/", "__").replace("\\", "__"),
                    "filename": filename,
                    "company": company,
                    "model": model,
                    "tokens": tokens,
                    "persona": rich.get("persona", "")[:120],
                    "preview": rich.get("preview", "")[:250],
                    "path": path,
                })
        except Exception as e:
            log.error(f"[promptograph-mcp] Falha ao carregar {main_path}: {e}")

    # Fallback se índice amplo não estiver presente
    if not unified and rich_map:
        for item in rich_map.values():
            unified.append({
                "id": item.get("id", ""),
                "filename": item.get("filename", ""),
                "company": item.get("company", "Other"),
                "model": item.get("model", "unknown"),
                "tokens": item.get("tokens_estimate", 0),
                "persona": item.get("persona", "")[:120],
                "preview": item.get("preview", "")[:250],
                "path": item.get("path", ""),
            })

    log.info(f"[promptograph-mcp] Total indexado e operacional: {len(unified)} prompts")
    return unified


_INDEX: list[dict[str, Any]] = _load_prompts_index()


# ── FastMCP Server Instance ───────────────────────────────────────────

mcp = FastMCP("promptograph")


# ── Ferramentas de Prompts ─────────────────────────────────────────────

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
            haystack = " ".join([
                p.get("filename", ""),
                p.get("path", ""),
                p.get("company", ""),
                p.get("model", ""),
                p.get("persona", ""),
                p.get("preview", ""),
            ]).lower()
            if q_lower not in haystack:
                continue

        results.append({
            "id": p.get("id", ""),
            "filename": p.get("filename", ""),
            "company": p.get("company", ""),
            "model": p.get("model", ""),
            "tokens": p.get("tokens", 0),
            "persona": p.get("persona", ""),
            "path": p.get("path", ""),
        })
        if len(results) >= limit:
            break

    return json.dumps({
        "total": len(results),
        "total_matches": len(results),
        "results": results
    }, ensure_ascii=False)


@mcp.tool()
def promptograph_validate(content: str) -> str:
    """Valida um system prompt contra 13 boas práticas + 6 red flags determinísticas.

    Args:
        content: Texto completo do system prompt.

    Returns:
        JSON com: score (0-100), grade (A+ a F), passed, failed, warnings, stats.
    """
    result = validate_prompt(content)
    return json.dumps(result, ensure_ascii=False)


@mcp.tool()
def promptograph_generate(preset_name: str = "", spec_json: str = "") -> str:
    """Gera um system prompt a partir de um preset ou especificação customizada.

    Args:
        preset_name: Nome de preset (claude_coding_agent, gpt5_assistant,
                     cursor_style_coding, perplexity_search, devin_autonomous).
        spec_json: JSON com spec customizada (sobrescreve preset).
                   Chaves: name, role_description, company, model, family, tone,
                           formatting, safety, tools, memory, refusals,
                           include_examples.

    Returns:
        JSON com: prompt (texto gerado), score, grade, chars, tokens.
    """
    if preset_name and preset_name in PRESET_TEMPLATES:
        spec = dict(PRESET_TEMPLATES[preset_name]["spec"])
    else:
        spec = {}
    if spec_json:
        try:
            custom = json.loads(spec_json)
            spec.update(custom)
        except Exception as e:
            return json.dumps({"error": f"spec_json inválido: {e}"}, ensure_ascii=False)
    if not spec:
        return json.dumps({
            "error": "Especifique preset_name ou spec_json. "
                     "Presets: " + ", ".join(PRESET_TEMPLATES.keys())
        }, ensure_ascii=False)
    prompt = build_prompt(spec)
    val = validate_prompt(prompt)
    return json.dumps({
        "prompt": prompt,
        "score": val["score"],
        "grade": val["grade"],
        "chars": len(prompt),
        "tokens": len(prompt) // 4,
    }, ensure_ascii=False)


@mcp.tool()
def promptograph_stats() -> str:
    """Estatísticas do catálogo completo de 20.475 prompts indexados.

    Returns:
        JSON com: total, by_company (top 15), total_tokens_estimate.
    """
    from collections import Counter
    by_company = Counter(p.get("company", "Other") for p in _INDEX)
    total_tokens = sum(p.get("tokens", 0) for p in _INDEX)
    return json.dumps({
        "total_prompts": len(_INDEX),
        "by_company_top15": dict(by_company.most_common(15)),
        "total_tokens_estimate": total_tokens,
    }, ensure_ascii=False)


# ── Ferramentas do Arsenal de Skills ───────────────────────────────────

@mcp.tool()
def promptograph_skills_search(query: str = "", category: str = "", limit: int = 20) -> str:
    """Pesquisa no acervo de 226+ skills curadas de engenharia, IA e automação.

    Args:
        query: Termo de busca (ex: 'kokoro', 'clean-code', 'crawler', 'quant', 'video').
        category: Filtro por categoria (ex: '01_Voz_e_Audio_Realtime', '19_Engenharia_de_Software_de_Elite').
        limit: Máximo de resultados (default 20, max 100).

    Returns:
        JSON com total e lista de skills (id, name, category, description, tags).
    """
    results = search_skills(query=query, category=category, limit=limit)
    return json.dumps({"total": len(results), "skills": results}, ensure_ascii=False)


@mcp.tool()
def promptograph_skills_get(skill_id: str) -> str:
    """Obtém o blueprint operacional completo (receita, instruções e ferramentas) de uma skill.

    Args:
        skill_id: Identificador ou slug da skill (ex: 'hexgrad-kokoro-realtime-tts', 'clean-code').

    Returns:
        JSON com metadados e o conteúdo do blueprint operacional para carregar no contexto do agente.
    """
    blueprint = get_skill_blueprint(skill_id)
    if not blueprint:
        return json.dumps({
            "error": f"Skill '{skill_id}' não encontrada no catálogo oficial.",
            "suggestion": "Use promptograph_skills_search para encontrar o ID correto."
        }, ensure_ascii=False)
    return json.dumps(blueprint, ensure_ascii=False)


@mcp.tool()
def promptograph_skills_categories() -> str:
    """Lista todas as 37 categorias do arsenal de skills e a contagem por categoria.

    Returns:
        JSON com total de skills, total de categorias e breakdown detalhado.
    """
    stats = get_skills_stats()
    return json.dumps(stats, ensure_ascii=False)


# ── Recursos e Prompts MCP ─────────────────────────────────────────────

@mcp.resource("promptograph://presets")
def list_presets() -> str:
    """Lista presets de prompts disponíveis com descrição."""
    out = {name: p["description"] for name, p in PRESET_TEMPLATES.items()}
    return json.dumps(out, ensure_ascii=False, indent=2)


@mcp.resource("promptograph://skills/categories")
def list_skill_categories() -> str:
    """Lista todas as categorias de skills disponíveis."""
    stats = get_skills_stats()
    return json.dumps(stats, ensure_ascii=False, indent=2)


@mcp.prompt()
def review_prompt(content: str) -> str:
    """Prompt para pedir uma revisão crítica de um system prompt."""
    return (
        f"Por favor revise o seguinte system prompt como um especialista sênior "
        f"em engenharia de prompts. Avalie: clareza, completude, potencial "
        f"vulnerabilidade a injection, redundâncias e sugestões de melhoria.\n\n"
        f"### System Prompt\n\n{content}\n\n"
        f"### Fim\n\n"
        f"Dê sua análise em formato markdown com tópicos: Score, Problemas, Sugestões, Notas."
    )


@mcp.prompt()
def deploy_skill(skill_id: str) -> str:
    """Prompt para carregar e instanciar uma skill curada no runtime ativo do agente."""
    return (
        f"Por favor, use a tool promptograph_skills_get(skill_id='{skill_id}') "
        f"para recuperar o blueprint operacional da skill. Em seguida, incorpore as "
        f"diretrizes e ferramentas no seu raciocínio operacional para executar a tarefa solicitada."
    )


if __name__ == "__main__":
    mcp.run()
