"""src/skills/promptograph/skills_registry.py — Registro e busca de skills curadas.

Gerencia o carregamento e pesquisa no manifesto de 226+ skills curadas
distribuídas em 37 categorias de engenharia, IA, multimídia e automação.
"""

from __future__ import annotations

import json
import logging
from collections import Counter
from pathlib import Path
from typing import Any

log = logging.getLogger("promptograph.skills_registry")

_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_MANIFEST_PATHS = [
    _ROOT / "data" / "promptograph" / "skills_manifest.json",
    _ROOT / "data" / "skills_manifest.json",
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
    for s in _SKILLS:
        # Filtro de categoria
        if cat_lower and cat_lower not in s.get("category", "").lower():
            continue

        # Busca textual
        if q_lower:
            haystack = " ".join([
                s.get("id", ""),
                s.get("name", ""),
                s.get("description", ""),
                " ".join(s.get("tags", [])),
                s.get("category", ""),
            ]).lower()
            if q_lower not in haystack:
                continue

        results.append({
            "id": s.get("id", ""),
            "name": s.get("name", ""),
            "category": s.get("category", ""),
            "description": s.get("description", "")[:200],
            "tags": s.get("tags", []),
        })

        if len(results) >= limit:
            break

    return results


def get_skill_blueprint(skill_id: str) -> dict[str, Any] | None:
    """Recupera o blueprint operacional completo de uma skill pelo ID ou slug."""
    _ensure_loaded()
    target = skill_id.lower().strip()

    for s in _SKILLS:
        if s.get("id", "").lower() == target or s.get("name", "").lower() == target:
            return s

    # Fallback: busca por correspondência parcial de ID
    for s in _SKILLS:
        if target in s.get("id", "").lower():
            return s

    return None


def get_skills_stats() -> dict[str, Any]:
    """Retorna estatísticas do catálogo de skills."""
    _ensure_loaded()
    by_category = Counter(s.get("category", "Outros") for s in _SKILLS)
    return {
        "total_skills": len(_SKILLS),
        "total_categories": len(by_category),
        "by_category": dict(by_category.most_common()),
    }
