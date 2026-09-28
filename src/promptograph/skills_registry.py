"""src/promptograph/skills_registry.py — Registro e busca de skills curadas.

Gerencia o carregamento e pesquisa no manifesto de 226+ skills curadas
distribuídas em 37 categorias de engenharia, IA, multimídia e automação.
Compatível com execução local no repositório e instalação via pacote PyPI / uvx.
"""

from __future__ import annotations

import json
import logging
from collections import Counter
from pathlib import Path
from typing import Any

log = logging.getLogger("promptograph.skills_registry")

_PKG_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _PKG_DIR.parent.parent

_MANIFEST_PATHS = [
    _PKG_DIR / "data" / "skills_manifest.json",
    _REPO_ROOT / "data" / "skills_manifest.json",
    _REPO_ROOT / "data" / "promptograph" / "skills_manifest.json",
]

_SKILLS: list[dict[str, Any]] = []


def _ensure_loaded() -> None:
    """Carrega o manifesto de skills na primeira chamada."""
    global _SKILLS
    if _SKILLS:
        return

    for path in _MANIFEST_PATHS:
        if path.exists():
            try:
                _SKILLS = json.loads(path.read_text(encoding="utf-8"))
                log.info(f"Carregadas {len(_SKILLS)} skills de {path}")
                return
            except Exception as e:
                log.error(f"Erro ao carregar {path}: {e}")

    log.warning("Nenhum arquivo skills_manifest.json encontrado.")
    _SKILLS = []


def search_skills(query: str = "", category: str = "", limit: int = 20) -> list[dict[str, Any]]:
    """Pesquisa skills por termo, tags e categoria.

    Args:
        query: Termo de busca (no id, nome, descrição ou tags).
        category: Filtro exato ou parcial de categoria.
        limit: Quantidade máxima de resultados (1-100).

    Returns:
        Lista de dicionários resumidos das skills encontradas.
    """
    _ensure_loaded()
    limit = max(1, min(int(limit), 100))
    q_lower = query.lower().strip()
    cat_lower = category.lower().strip()

    results = []
    for skill in _SKILLS:
        if cat_lower and cat_lower not in skill.get("category", "").lower():
            continue

        if q_lower:
            text_corpus = " ".join([
                skill.get("id", ""),
                skill.get("name", ""),
                skill.get("description", ""),
                " ".join(skill.get("tags", [])),
                skill.get("category", ""),
            ]).lower()
            if q_lower not in text_corpus:
                continue

        results.append({
            "id": skill.get("id"),
            "name": skill.get("name"),
            "category": skill.get("category"),
            "description": skill.get("description", "")[:200] + "..." if len(skill.get("description", "")) > 200 else skill.get("description", ""),
            "tags": skill.get("tags", []),
            "has_blueprint": bool(skill.get("blueprint")),
        })
        if len(results) >= limit:
            break

    return results


def get_skill_blueprint(skill_id: str) -> dict[str, Any] | None:
    """Recupera os detalhes completos e o blueprint executável (SKILL.md) de uma skill.

    Args:
        skill_id: ID exato ou relativo da skill.

    Returns:
        Dicionário com metadados e o conteúdo integral do blueprint markdown.
    """
    _ensure_loaded()
    sid_lower = skill_id.lower().strip()

    for skill in _SKILLS:
        if skill.get("id", "").lower() == sid_lower or skill.get("name", "").lower() == sid_lower:
            return {
                "id": skill.get("id"),
                "name": skill.get("name"),
                "category": skill.get("category"),
                "description": skill.get("description"),
                "tags": skill.get("tags", []),
                "relative_path": skill.get("relative_path"),
                "blueprint": skill.get("blueprint", ""),
            }

    return None


def get_skills_stats() -> dict[str, Any]:
    """Retorna estatísticas de contagem e distribuição por categoria."""
    _ensure_loaded()
    cats = Counter(s.get("category", "Outras") for s in _SKILLS)
    return {
        "total_skills": len(_SKILLS),
        "total_categories": len(cats),
        "categories_distribution": dict(cats.most_common()),
    }
