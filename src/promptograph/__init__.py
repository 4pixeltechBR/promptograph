"""promptograph — Engenharia reversa, validação heurística e hub MCP de system prompts e skills curadas.

Organização: 4pixeltechBR
Repositório: https://github.com/4pixeltechBR/promptograph
"""

from __future__ import annotations

__version__ = "0.3.2"

from promptograph.validator import validate_prompt, GOOD_PRACTICES, RED_FLAGS
from promptograph.builder import build_prompt, PRESET_TEMPLATES, TEMPLATES
from promptograph.skills_registry import (
    search_skills,
    get_skill_blueprint,
    get_skills_stats,
)

__all__ = [
    "__version__",
    "validate_prompt",
    "GOOD_PRACTICES",
    "RED_FLAGS",
    "build_prompt",
    "PRESET_TEMPLATES",
    "TEMPLATES",
    "search_skills",
    "get_skill_blueprint",
    "get_skills_stats",
]
