---
name: promptograph
description: Ferramenta para navegar, comparar (diff), validar deterministicamente (0-100%, 13 regras heurísticas) e gerar system prompts de IA de nível de produção. Construída sobre uma base de 5.317 system prompts reais (Anthropic, OpenAI, Google, Cursor, xAI, etc.) totalizando 12M de tokens. Inclui servidor FastMCP com 4 tools, CLI de busca e interface web offline zero-dependency.
license: MIT
metadata:
  author: 4PixelTech
  version: 0.2.0
  prompts_indexed: 5317
  tokens_estimate: 12098882
---

# 📷 Promptograph — Engenharia Reversa, Validação & Geração de System Prompts

O **Promptograph** é a ferramenta definitiva para engenharia reversa, análise constitucional, validação heurística e síntese de **System Prompts** de IA. Desenvolvido sobre uma base indexada de **5.317 system prompts reais de produção** (mais de 12 milhões de tokens) extraídos das principais empresas de IA do mundo (Anthropic, OpenAI, Google, Cursor, xAI, Perplexity, etc.).

---

## 🏛️ Capacidades Centrais

1. **📚 Browse & Search:** Busca semântica e lexical em 5.317 prompts por empresa, modelo, persona ou palavras-chave.
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
3. **✨ Generative Presets:** Gerador de prompts estruturados com base em presets validados (ex: `claude_coding_agent`, `openai_researcher`, `expert_tutor`).
4. **🔌 FastMCP Server (Model Context Protocol):** Servidor pronto para conectar agentes com 4 ferramentas nativas.
5. **🌐 Interface Web Offline Zero-Dependency:** Dashboard local completo em Python sem necessidade de npm/pip.

---

## 🛠️ Como Utilizar via Terminal

### 1. Busca Rápida no Catálogo de 5.317 Prompts
```bash
# Buscar system prompts por palavra-chave (ex: cursor, claude, security)
python "E:\Skills\11_Engenharia_de_Prompts_e_Sabedoria\promptograph\scripts\search_promptograph.py" "cursor"

# Filtrar por empresa
python "E:\Skills\11_Engenharia_de_Prompts_e_Sabedoria\promptograph\scripts\search_promptograph.py" "agent" --company Anthropic

# Ver estatísticas completas dos 5.317 prompts
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

### 4. Iniciar Servidor Web Offline
```bash
python "E:\Skills\11_Engenharia_de_Prompts_e_Sabedoria\promptograph\server.py"
# Acesse no navegador: http://localhost:8000
```

---

## 🔌 Servidor FastMCP (`scripts/promptograph_mcp_server.py`)

O servidor FastMCP expõe 4 ferramentas via `stdio`:
* `promptograph_search(query, company, model, limit)`: Retorna prompts indexados com metadados.
* `promptograph_validate(content)`: Avalia o prompt e retorna score, nota e falhas específicas.
* `promptograph_generate(preset_name, spec_json)`: Gera novo prompt validado a partir de templates.
* `promptograph_stats()`: Retorna métricas globais e distribuição de modelos/empresas.

### Configuração no `mcp_servers.json` / Claude Desktop / Antigravity:
```json
{
  "promptograph": {
    "command": "python",
    "args": [
      "E:\\Skills\\11_Engenharia_de_Prompts_e_Sabedoria\\promptograph\\scripts\\promptograph_mcp_server.py"
    ]
  }
}
```

---

## 🐍 Uso Programático em Python

```python
from pathlib import Path
import sys
sys.path.insert(0, r"E:\Skills\11_Engenharia_de_Prompts_e_Sabedoria\promptograph")

from src.skills.promptograph import validate_prompt, build_prompt, PRESET_TEMPLATES

# Validar qualquer prompt
resultado = validate_prompt("You are an AI assistant...")
print(f"Nota: {resultado['grade']} ({resultado['score']}%)")

# Gerar prompt customizado
spec = PRESET_TEMPLATES['claude_coding_agent']['spec']
prompt_gerado = build_prompt(spec)
```
