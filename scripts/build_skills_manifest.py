#!/usr/bin/env python3
"""scripts/build_skills_manifest.py — Gerador do Manifesto de Skills para o Promptograph MCP.

Varre as categorias seguras e aprovadas de E:\\Skills, extrai metadados e receitas operacionais
dos arquivos SKILL.md e gera os arquivos:
  - data/promptograph/skills_manifest.json (catálogo completo com blueprints)
  - data/promptograph/skills_summary.json (índice compacto para busca rápida)

Identidade: 4pixeltechBR
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SKILLS_ROOT = Path(r"E:\Skills")
_OUTPUT_DIR = _REPO_ROOT / "data" / "promptograph"
_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Categorias aprovadas (Verdes + Amarelas saneadas + Falsos positivos de negócio/arquitetura)
# Categorias estritamente proibidas por ToS do GitHub NUNCA são incluídas aqui.
EXCLUDED_CATEGORIES = {
    "10_Ciberseguranca_OSINT_e_Forense",
    "33_DarkArts_Engenharia_Oculta_e_Vanguarda_Extrema",
    "36_Automacao_Subterranea_Furtiva_e_Escala_Extrema",
    "42_Computacao_Forense_Fisica_e_Dump_de_Memoria",
}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extrai frontmatter YAML simples e corpo markdown."""
    match = FRONTMATTER_RE.match(content)
    if not match:
        return {}, content
    
    fm_text = match.group(1)
    body = content[match.end():]
    data = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            data[key] = val
    return data, body


def extract_title_and_desc_from_markdown(body: str) -> tuple[str, str]:
    """Extrai título H1 e primeiro parágrafo relevante do markdown."""
    title = ""
    description = ""
    lines = body.splitlines()
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not title and line_clean.startswith("# "):
            title = line_clean.replace("# ", "").strip()
            continue
        if title and not description and line_clean and not line_clean.startswith("#") and not line_clean.startswith("---"):
            description = line_clean[:280]
            break
    return title, description


def clean_blueprint(body: str, max_chars: int = 1500) -> str:
    """Retorna uma versão limpa e resumida do blueprint para o MCP."""
    cleaned = body.strip()
    if len(cleaned) > max_chars:
        return cleaned[:max_chars] + "\n\n... [Blueprint truncado para otimização de tokens de contexto. Consulte o repositório oficial]."
    return cleaned


def main() -> None:
    if not _SKILLS_ROOT.exists():
        logging.error(f"Diretório {_SKILLS_ROOT} não encontrado.")
        sys.exit(1)

    logging.info(f"Varrendo categorias em {_SKILLS_ROOT}...")
    categories = sorted([
        d for d in os.listdir(_SKILLS_ROOT)
        if os.path.isdir(_SKILLS_ROOT / d) and not d.startswith(".") and d not in EXCLUDED_CATEGORIES
    ])

    skills_manifest: list[dict] = []
    skills_summary: list[dict] = []
    categories_stats: dict[str, int] = {}

    for cat in categories:
        cat_path = _SKILLS_ROOT / cat
        cat_skills_count = 0

        # Subpastas de cada categoria
        subfolders = [
            f for f in os.listdir(cat_path)
            if os.path.isdir(cat_path / f) and not f.startswith(".")
        ]

        for folder in subfolders:
            skill_folder = cat_path / folder
            skill_md = skill_folder / "SKILL.md"
            if not skill_md.exists():
                continue

            try:
                raw_text = skill_md.read_text(encoding="utf-8", errors="replace")
            except Exception as e:
                logging.warning(f"Erro ao ler {skill_md}: {e}")
                continue

            fm, body = parse_frontmatter(raw_text)
            h1_title, md_desc = extract_title_and_desc_from_markdown(body)

            skill_id = fm.get("name") or folder
            skill_name = h1_title or skill_id.replace("-", " ").title()
            description = fm.get("description") or md_desc or f"Skill operacional para {skill_name}"
            tools_spec = fm.get("tools", "")

            # Tags inferidas
            tags = [cat.split("_", 1)[-1].lower()]
            for word in skill_id.split("-"):
                if len(word) > 3 and word.lower() not in tags:
                    tags.append(word.lower())

            full_entry = {
                "id": skill_id,
                "name": skill_name,
                "category": cat,
                "description": description,
                "tools": tools_spec,
                "tags": tags[:6],
                "blueprint": clean_blueprint(body),
            }

            summary_entry = {
                "id": skill_id,
                "name": skill_name,
                "category": cat,
                "description": description[:180],
                "tags": tags[:4],
            }

            skills_manifest.append(full_entry)
            skills_summary.append(summary_entry)
            cat_skills_count += 1

        if cat_skills_count > 0:
            categories_stats[cat] = cat_skills_count

    # Gravar manifestos
    manifest_path = _OUTPUT_DIR / "skills_manifest.json"
    summary_path = _OUTPUT_DIR / "skills_summary.json"

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(skills_manifest, f, indent=2, ensure_ascii=False)

    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(skills_summary, f, indent=2, ensure_ascii=False)

    # Copiar também para data/ raiz para compatibilidade
    root_data = _REPO_ROOT / "data"
    with open(root_data / "skills_manifest.json", "w", encoding="utf-8") as f:
        json.dump(skills_manifest, f, indent=2, ensure_ascii=False)

    with open(root_data / "skills_summary.json", "w", encoding="utf-8") as f:
        json.dump(skills_summary, f, indent=2, ensure_ascii=False)

    manifest_size_kb = manifest_path.stat().st_size / 1024
    summary_size_kb = summary_path.stat().st_size / 1024

    logging.info("=" * 60)
    logging.info(f"MANIFESTO CONCLUÍDO COM SUCESSO:")
    logging.info(f"  Categorias cobertas : {len(categories_stats)}")
    logging.info(f"  Total de Skills     : {len(skills_manifest)}")
    logging.info(f"  skills_manifest.json: {manifest_size_kb:.1f} KB")
    logging.info(f"  skills_summary.json : {summary_size_kb:.1f} KB")
    logging.info("=" * 60)


if __name__ == "__main__":
    main()
