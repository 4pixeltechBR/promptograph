---
name: promptograph
description: Ferramenta para navegar, comparar (diff), validar deterministicamente (0-100%, 13 regras heurísticas) e gerar system prompts de IA de nível de produção. Construída sobre uma base de 20.475 system prompts reais (Anthropic, OpenAI, Google, Cursor, xAI, Meta, DeepSeek, etc.) totalizando mais de 94M de tokens, além de um registro integrado de 226+ skills curadas em 37 domínios. Inclui servidor FastMCP com 7 tools, CLI de busca e interface web offline zero-dependency.
license: MIT
metadata:
  author: 4PixelTech
  version: 0.3.1
  prompts_indexed: 20475
  curated_skills: 226
  skill_domains: 37
  tokens_estimate: 97040739
---

# 📷 Promptograph — Engenharia Reversa, Validação, Geração de System Prompts & Hub de Skills MCP

O **Promptograph** é a ferramenta definitiva para engenharia reversa, análise constitucional, validação heurística, síntese de **System Prompts** de IA e distribuição de **Skills Curadas para Agentes**. Desenvolvido sobre uma base indexada de **20.475 system prompts reais de produção** (mais de 94 milhões de tokens) de 55 repositórios públicos (Anthropic, OpenAI, Google, Cursor, xAI, Meta, DeepSeek, Perplexity, etc.) e um manifesto operacional de **226 skills curadas em 37 categorias**.

---

## 🏛️ Capacidades Centrais

1. **📚 Browse & Search:** Busca em 20.475 prompts por empresa, modelo, persona ou palavras-chave.
2. **✅ Heuristic Validation:** Pontuação determinística de 0 a 100% (notas A+ a F) baseada em 13 padrões estruturais de prompts em produção:
   - Identidade e persona clara
   - Diretrizes de tom de voz
   - Regras explícitas de segurança
   - Limites operacionais (o que NÃO fazer)
   - Knowledge cutoff e ancoragem temporal
   - Regras de formatação (Markdown, bullets vs prosa)
   - Política de recusa objetiva sem sermão
   - Documentação de ferramentas (Tool use)
   - Seção de exemplos few-shot (`<example>`)
   - Gestão de memória/contexto silenciosa
   - Organização por tags XML estruturadas
   - Regras de citação e verificação de fontes
   - Proteção contra jailbreak e prompt injection
3. **✨ Generative Presets:** Gerador de prompts estruturados com base em presets validados (ex: `claude_coding_agent`, `gpt5_assistant`, `cursor_style_coding`, `perplexity_search`, `devin_autonomous`).
4. **🔌 FastMCP Server (Model Context Protocol):** Servidor pronto para conectar agentes com 7 ferramentas nativas (busca de prompts, validação, geração e injeção dinâmica de skills operacionais).
5. **🧩 Curated Skills Registry:** Manifesto operacional com 226 skills em 37 domínios de engenharia, áudio, vídeo, automação e código limpo.
6. **🌐 Interface Web Offline Zero-Dependency:** Dashboard local completo em Python stdlib com visualização de prompts, diff side-by-side e catálogo interativo de skills.

---

## 🛠️ Como Utilizar via Terminal

### 1. Busca Rápida no Catálogo de 20.475 Prompts
```bash
# Buscar system prompts por palavra-chave (ex: cursor, claude, security)
python "E:\Skills\11_Engenharia_de_Prompts_e_Sabedoria\promptograph\scripts\search_promptograph.py" "cursor"

# Filtrar por empresa
python "E:\Skills\11_Engenharia_de_Prompts_e_Sabedoria\promptograph\scripts\search_promptograph.py" "agent" --company Anthropic

# Ver estatísticas completas dos 20.475 prompts
python "E:\Skills\11_Engenharia_de_Prompts_e_Sabedoria\promptograph\scripts\search_promptograph.py" --stats
```

### 2. Validar Heuristicamente um System Prompt
```bash
python "E:\Skills\11_Engenharia_de_Prompts_e_Sabedoria\promptograph\scripts\search_promptograph.py" --validate "You are Claude, an AI assistant built by Anthropic..."
```

### 3. Gerar um System Prompt a partir de Preset
```bash
python "E:\Skills\11_Engenharia_de_Prompts_e_Sabedoria\promptograph\scripts\search_promptograph.py" --generate claude_coding_agent
```

### 4. Iniciar Servidor Web Standalone
```bash
python "E:\Skills\11_Engenharia_de_Prompts_e_Sabedoria\promptograph\server.py" 8765
# Acesse no navegador: http://localhost:8765
```

---

## 🔌 Servidor FastMCP (`scripts/promptograph_mcp_server.py`)

O servidor FastMCP expõe 7 ferramentas via `stdio`:
* `promptograph_search(query, company, model, limit)`: Busca em 20.475 prompts de produção.
* `promptograph_validate(content)`: Avalia o prompt e retorna score (0-100%), nota e falhas específicas.
* `promptograph_generate(preset_name, spec_json)`: Gera novo prompt validado a partir de templates.
* `promptograph_stats()`: Retorna métricas globais e distribuição de modelos/empresas.
* `promptograph_skills_search(query, category, limit)`: Busca no acervo de 226 skills curadas.
* `promptograph_skills_get(skill_id)`: Retorna o blueprint operacional executável (`SKILL.md`).
* `promptograph_skills_categories()`: Relatório das 37 categorias técnicas disponíveis.

### Configuração no `mcp_servers.json` / Claude Desktop / Cursor / Antigravity:
```json
{
  "mcpServers": {
    "promptograph": {
      "command": "python",
      "args": [
        "E:\\Skills\\11_Engenharia_de_Prompts_e_Sabedoria\\promptograph\\scripts\\promptograph_mcp_server.py"
      ]
    }
  }
}
```

---

## 🐍 Uso Programático em Python

```python
from pathlib import Path
import sys
sys.path.insert(0, r"E:\Skills\11_Engenharia_de_Prompts_e_Sabedoria\promptograph")

from src.skills.promptograph import (
    validate_prompt,
    build_prompt,
    PRESET_TEMPLATES,
    search_skills,
    get_skill_blueprint,
)

# 1. Validar qualquer prompt
resultado = validate_prompt("You are an AI assistant...")
print(f"Nota: {resultado['grade']} ({resultado['score']}%)")

# 2. Gerar prompt customizado
spec = PRESET_TEMPLATES['claude_coding_agent']['spec']
prompt_gerado = build_prompt(spec)

# 3. Buscar skills do catálogo
skills_encontradas = search_skills("clean-code")
blueprint = get_skill_blueprint("clean-code")
```
