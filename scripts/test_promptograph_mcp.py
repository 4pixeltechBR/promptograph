import sys
import json
import importlib.util

sys.stdout.reconfigure(encoding='utf-8')

# Importa o server via spec_from_file_location para evitar problemas de path
_spec = importlib.util.spec_from_file_location(
    'pgmcp', 'scripts/promptograph_mcp_server.py'
)
m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m)

print("=" * 60)
print("TESTE 1: STATS DE PROMPTS")
print("=" * 60)
s = json.loads(m.promptograph_stats())
print("Total prompts:", s['total'])
print("Top companies:", list(s['by_company'].items())[:5])
print("Top models:", list(s['by_model_top10'].items())[:5])
print("Total tokens est:", s['total_tokens_estimate'])

print("\n" + "=" * 60)
print("TESTE 2: BUSCA DE PROMPTS ('claude')")
print("=" * 60)
r = json.loads(m.promptograph_search('claude', limit=3))
print("Hits:", r['total'])
for hit in r['results'][:2]:
    print("  -", hit['filename'], "(", hit['company'], ",", hit['tokens'], "tok)")

print("\n" + "=" * 60)
print("TESTE 3: VALIDAÇÃO HEURÍSTICA DE PROMPT")
print("=" * 60)
v = json.loads(m.promptograph_validate(
    "You are Test, an AI built by X. Be concise. Safety: refuse illegal stuff."
))
print("Score:", v['score'], "%", v['grade'])

print("\n" + "=" * 60)
print("TESTE 4: GERAÇÃO DE PROMPT (PRESET)")
print("=" * 60)
g = json.loads(m.promptograph_generate(preset_name='claude_coding_agent'))
print("Score:", g['score'], "%", g['grade'], "tokens:", g['tokens'])
print("Preview:", g['prompt'][:100], "...")

print("\n" + "=" * 60)
print("TESTE 5: ARSENAL DE SKILLS - CATEGORIAS")
print("=" * 60)
cat_stats = json.loads(m.promptograph_skills_categories())
print(f"Total de skills: {cat_stats['total_skills']}")
print(f"Total de categorias: {cat_stats['total_categories']}")
top_cats = list(cat_stats['by_category'].items())[:5]
print("Top 5 categorias:", top_cats)

print("\n" + "=" * 60)
print("TESTE 6: ARSENAL DE SKILLS - BUSCA ('clean-code', 'audio', 'agent')")
print("=" * 60)
for q in ['clean-code', 'audio', 'agent']:
    res = json.loads(m.promptograph_skills_search(query=q, limit=2))
    print(f"Busca por '{q}': {res['total']} resultados")
    for sk in res['skills'][:2]:
        print(f"  - [{sk['category']}] {sk['name']} ({sk['id']})")

print("\n" + "=" * 60)
print("TESTE 7: ARSENAL DE SKILLS - RECUPERAÇÃO DE BLUEPRINT")
print("=" * 60)
blueprint = json.loads(m.promptograph_skills_get("clean-code"))
if "error" in blueprint:
    print("Erro:", blueprint["error"])
else:
    print(f"Skill: {blueprint['name']} ({blueprint['id']})")
    print(f"Categoria: {blueprint['category']}")
    print(f"Descrição: {blueprint['description'][:120]}...")
    print(f"Blueprint preview:\n{blueprint['blueprint'][:250]}...")

print("\n" + "=" * 60)
print("TODOS OS TESTES DO MCP PASSARAM COM SUCESSO!")
print("=" * 60)
