"""promptograph skill — validação, geração e registro MCP de system prompts e skills.

Port do projeto Promptograph (MIT, github.com/4pixeltechBR/promptograph).
Baseado em 20.475 prompts reais de produção e 226+ skills curadas de engenharia e IA.

Módulos:
- validator: 13 boas práticas + 6 red flags (score 0-100%, grade A+ a F)
- builder:    5 presets (Claude/GPT/Cursor/Perplexity/Devin) + templates modulares
- skills_registry: Busca e recuperação de blueprints das 226+ skills do arsenal
"""

from __future__ import annotations

from src.skills.promptograph.validator import validate_prompt, GOOD_PRACTICES, RED_FLAGS
from src.skills.promptograph.builder import build_prompt, PRESET_TEMPLATES, TEMPLATES
from src.skills.promptograph.skills_registry import (
    search_skills,
    get_skill_blueprint,
    get_skills_stats,
)

__all__ = [
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
