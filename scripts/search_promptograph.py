#!/usr/bin/env python3
"""
CLI de busca e validacao rapida para o acervo Promptograph (20.475 system prompts reais).
Uso:
    python search_promptograph.py [termo]
    python search_promptograph.py "claude" --company Anthropic
    python search_promptograph.py --validate "You are an assistant..."
    python search_promptograph.py --stats
    python search_promptograph.py --generate claude_coding_agent
"""

import os
import sys
import json
import argparse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

from src.skills.promptograph import validate_prompt, build_prompt, PRESET_TEMPLATES

_INDEX_PATH = _ROOT / "data" / "index_filtered.json"

def load_index():
    candidates = [
        _INDEX_PATH,
        _ROOT / "data" / "promptograph" / "index_filtered.json",
        Path(r"E:\Skills\11_Engenharia_de_Prompts_e_Sabedoria\promptograph\data\index_filtered.json"),
    ]
    for p in candidates:
        if p.exists():
            raw = json.loads(p.read_text(encoding="utf-8", errors="ignore"))
            if isinstance(raw, dict):
                return raw.get("entries", [])
            return raw
    print("Erro: indice nao encontrado em nenhum dos caminhos conhecidos.")
    sys.exit(1)

def show_stats():
    data = load_index()
    total = len(data)
    companies = {}
    models = {}
    total_tokens = 0
    
    for item in data:
        c = item.get("company") or "Other"
        companies[c] = companies.get(c, 0) + 1
        m = item.get("model") or "unknown"
        models[m] = models.get(m, 0) + 1
        toks = item.get("tokens")
        if toks is None:
            toks = int(item.get("words", 0) * 4 // 3)
        total_tokens += int(toks or 0)
        
    print("=" * 65)
    print("📷 PROMPTOGRAPH — ESTATISTICAS DO INDICE DE SYSTEM PROMPTS (v0.3.1)")
    print("=" * 65)
    print(f"Total de Prompts Indexados: {total:,}")
    print(f"Volume Estimado de Tokens:   {total_tokens:,} tokens (~97M)")
    print("\nDistribuicao por Empresa / Lab:")
    for comp, count in sorted(companies.items(), key=lambda x: x[1], reverse=True)[:8]:
        pct = (count / total) * 100 if total else 0
        print(f"  • {comp:<20} : {count:5d} ({pct:5.1f}%)")
        
    print("\nModelos mais frequentes:")
    for mod, count in sorted(models.items(), key=lambda x: x[1], reverse=True)[:8]:
        print(f"  • {mod:<20} : {count:5d}")
    print("=" * 65)

def search(query, company=None, model=None, limit=20, full=False):
    data = load_index()
    q_lower = query.lower().strip() if query else ""
    comp_lower = company.lower().strip() if company else None
    mod_lower = model.lower().strip() if model else None
    
    results = []
    for item in data:
        if comp_lower and comp_lower not in (item.get("company") or "").lower():
            continue
        if mod_lower and mod_lower not in (item.get("model") or "").lower():
            continue
            
        fname = item.get("filename", "")
        persona = item.get("persona", "")
        preview = item.get("preview", "")
        
        if not q_lower or (q_lower in fname.lower() or q_lower in persona.lower() or q_lower in preview.lower()):
            results.append(item)
            
    print(f"\nBusca por '{query or '*'}' (Empresa: {company or 'todas'}, Modelo: {model or 'todos'})")
    print(f"Total de correspondencias: {len(results)} (Exibindo ate {limit})\n" + "=" * 65)
    
    for i, item in enumerate(results[:limit], 1):
        fn = item.get("filename", "sem_nome")
        comp = item.get("company", "Other")
        mod = item.get("model", "unknown")
        toks = item.get("tokens", 0)
        persona = item.get("persona", "") or "Geral"
        preview = item.get("preview", "").replace("\n", " ").strip()
        
        print(f"[{i}] {fn} | {comp} | Modelo: {mod} | {toks:,} tokens")
        print(f"    Persona: {persona}")
        if full:
            print(f"    Previa:\n    {preview[:500]}...")
        else:
            print(f"    Previa: {preview[:140]}...")
        print()

def validate_text(text):
    res = validate_prompt(text)
    print("=" * 65)
    print("🔍 RELATORIO DE VALIDACAO HEURISTICA DE SYSTEM PROMPT")
    print("=" * 65)
    print(f"Nota Final: {res['grade']} ({res['score']}%)")
    print(f"Passou em:  {len(res['passed'])}/13 regras")
    print(f"Avisos:     {len(res['warnings'])}")
    print(f"Falhas:     {len(res['failed'])}")
    print(f"Diagnostico: {res['summary']}")
    print("\nRegras Aprovadas:")
    for p in res.get('passed', []):
        print(f"  [OK] {p.get('key')} -> {p.get('description', '')}")
    if res.get('failed'):
        print("\nRegras que Falharam:")
        for f in res.get('failed', []):
            print(f"  [FALHA] {f.get('key')} -> {f.get('description', '')}")
    if res.get('warnings'):
        print("\nAvisos:")
        for w in res.get('warnings', []):
            print(f"  [AVISO] {w.get('key')} -> {w.get('description', '')}")
    print("=" * 65)

def generate_preset(preset_name):
    if preset_name not in PRESET_TEMPLATES:
        print(f"Erro: preset '{preset_name}' desconhecido.")
        print(f"Presets disponiveis: {list(PRESET_TEMPLATES.keys())}")
        return
    prompt = build_prompt(PRESET_TEMPLATES[preset_name]['spec'])
    v = validate_prompt(prompt)
    print("=" * 65)
    print(f"✨ PROMPT GERADO — PRESET: {preset_name}")
    print(f"Score Heuristico: {v['score']}% ({v['grade']}) | Tokens est: {v['stats']['tokens_estimate']}")
    print("=" * 65)
    print(prompt)

def main():
    parser = argparse.ArgumentParser(description="Promptograph — 20.475 System Prompts Reais & Validacao Heuristica")
    parser.add_argument("query", nargs="?", default="", help="Termo para buscar nos prompts")
    parser.add_argument("--company", type=str, default=None, help="Filtrar por empresa (Anthropic, OpenAI, Google, etc)")
    parser.add_argument("--model", type=str, default=None, help="Filtrar por modelo (gpt-4, o3, claude, etc)")
    parser.add_argument("--limit", type=int, default=15, help="Limite de resultados (default: 15)")
    parser.add_argument("--full", action="store_true", help="Exibir previa mais detalhada")
    parser.add_argument("--stats", action="store_true", help="Exibir estatisticas completas do indice")
    parser.add_argument("--validate", type=str, default=None, help="Validar uma string de system prompt")
    parser.add_argument("--generate", type=str, default=None, help="Gerar prompt a partir de preset (ex: claude_coding_agent)")
    
    args = parser.parse_args()
    
    if args.stats:
        show_stats()
    elif args.validate:
        validate_text(args.validate)
    elif args.generate:
        generate_preset(args.generate)
    elif args.query or args.company or args.model:
        search(args.query, args.company, args.model, args.limit, args.full)
    else:
        show_stats()
        print("\nDica: execute com --help para ver todos os comandos de busca e validacao.")

if __name__ == "__main__":
    main()
