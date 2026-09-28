# 📷 Promptograph

> **Photograph every system prompt that matters & Equip AI Agents with Curated Skills.**  
> A production toolkit, Python package, and **FastMCP Server** to **browse**, **diff**, **validate**, and **generate** AI system prompts.  
> Built on **20,475 real-world system prompts** from 55 public repositories (~94M tokens), plus instant access to **226+ curated engineering skills** across 37 domains.

[![PyPI version](https://img.shields.io/pypi/v/promptograph.svg?color=blue)](https://pypi.org/project/promptograph/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Prompts indexed](https://img.shields.io/badge/prompts-20%2C475-brightgreen.svg)](#-verified-metrics--breakdown)
[![Skills indexed](https://img.shields.io/badge/skills-226%2B-blueviolet.svg)](#-verified-metrics--breakdown)
[![Skill domains](https://img.shields.io/badge/domains-37-purple.svg)](#-verified-metrics--breakdown)
[![FastMCP 7 Tools](https://img.shields.io/badge/MCP-7_Tools_Ready-orange.svg)](#-fastmcp-server-for-autonomous-agents)
[![Zero install](https://img.shields.io/badge/zero--install-uvx_ready-success.svg)](#-10-second-quick-start)
[![Live Site](https://img.shields.io/badge/site-live-blueviolet)](https://4pixeltechBR.github.io/promptograph/)

---

### Navigation / Navegação
[🇺🇸 English](#-english) · [🇧🇷 Português](#-português)

---

## 🇺🇸 English

### What is Promptograph?

**Promptograph** is a production toolkit that eliminates guesswork from prompt engineering and equips autonomous AI coding agents with ready-to-run engineering skills.

It resolves three fundamental challenges in generative AI:
1. **The Black-Box Problem:** Most teams guess how to prompt models. Promptograph gives you indexed, searchable access to **20,475 real-world production system prompts** extracted from 55 public repositories (including Anthropic, OpenAI, Google, Cursor, xAI, Meta, DeepSeek, Perplexity, and Cognition).
2. **Prompt Quality & Security Risks:** How do you know if your system prompt is robust before launching to production? Promptograph's **deterministic heuristic validator** audits prompts against 13 production-proven criteria and 6 red flags (scoring 0–100%, Grade A+ to F).
3. **Agent Capability Amnesia:** AI coding agents (Claude Desktop, Cursor, Windsurf, Claude Code, Antigravity) are powerful but lack domain-specific operational recipes. Promptograph functions as a plug-and-play **FastMCP Server** streaming **226+ operational skills** across 37 domains directly into your agent's reasoning loop.

---

### ⚡ 10-Second Quick Start

Promptograph is published on **PyPI** and requires **zero installation** when invoked via `uvx`:

#### 1. Instant CLI Search (No clone required)
```bash
# Search across 20,475 real production prompts
uvx promptograph search "claude coding"

# Validate any prompt against 13 heuristic rules
uvx promptograph validate "You are an expert coder. Answer briefly."

# Check corpus metrics and token distributions
uvx promptograph stats
```

#### 2. Launch Local Web Dashboard
```bash
uvx promptograph web 8765
# Open http://localhost:8765 in your browser
```

#### 3. Standard Pip Installation
```bash
pip install promptograph
# Or using uv:
uv add promptograph
```

---

### 🔌 FastMCP Server for Autonomous Agents

Promptograph implements the **Model Context Protocol (MCP)** using `FastMCP` over `stdio`. It connects directly to **Claude Desktop**, **Cursor**, **Windsurf**, **Claude Code**, and **Antigravity**.

#### Zero-Install MCP Configuration (Recommended)
Add this snippet to your agent's MCP configuration (`claude_desktop_config.json`, `.cursor/mcp.json`, etc.):

```json
{
  "mcpServers": {
    "promptograph": {
      "command": "uvx",
      "args": ["promptograph"]
    }
  }
}
```

#### Local Clone Configuration (Alternative)
If you prefer running from a local git clone:
```json
{
  "mcpServers": {
    "promptograph": {
      "command": "python",
      "args": ["/path/to/promptograph/scripts/promptograph_mcp_server.py"]
    }
  }
}
```

---

### 🛠️ The 7 MCP Agent Tools

When connected via MCP, your AI assistant receives 7 native callable tools:

| Tool | Category | Parameters | Purpose |
|---|---|---|---|
| `promptograph_search` | Prompts | `query`, `company`, `model`, `limit` | Searches 20,475 real prompts by lab, model, persona, or keyword |
| `promptograph_validate` | Quality | `content` | Evaluates prompt quality (0–100%, Grade A+ to F) checking 13 rules & 6 red flags |
| `promptograph_generate` | Synthesis | `preset_name`, `spec_json` | Generates robust prompts using battle-tested presets (Claude, GPT, Cursor, Devin) |
| `promptograph_stats` | Metrics | — | Returns live corpus metrics, token counts, and lab distributions |
| `promptograph_skills_search` | Skills | `query`, `category`, `limit` | Discovers relevant blueprints among 226+ curated engineering skills |
| `promptograph_skills_get` | Skills | `skill_id` | Streams the full executable markdown blueprint (`SKILL.md`) into agent context |
| `promptograph_skills_categories`| Skills | — | Lists all 37 technical domains with skill distribution counts |

#### Example Prompts to give your Agent:
* *"Search Promptograph for how Anthropic instructs Claude to handle tool-use errors."*
* *"Validate this system prompt before I deploy it to our customer support chatbot."*
* *"Look up a clean-code skill in Promptograph and apply its refactoring principles to this file."*

---

### 🐍 Python Library Usage

You can import Promptograph directly into your Python backend or custom agent pipeline without spinning up an MCP server:

```python
from promptograph import (
    validate_prompt,
    build_prompt,
    search_skills,
    get_skill_blueprint,
    get_skills_stats,
    PRESET_TEMPLATES,
)

# 1. Audit a system prompt programmatically
report = validate_prompt("You are a helpful assistant made by Acme Corp. Refuse harmful queries.")
print(f"Score: {report['score']}% (Grade: {report['grade']})")
print(f"Passed rules: {len(report['passed'])}/13")

# 2. Discover and retrieve curated skills
matches = search_skills(query="clean-code")
if matches:
    skill = get_skill_blueprint(matches[0]["id"])
    print(f"Skill: {skill['name']} [{skill['category']}]")
    print(skill["blueprint"][:400])  # Markdown recipe with executable code

# 3. Synthesize a production prompt from a preset
preset_spec = PRESET_TEMPLATES["claude_coding_agent"]["spec"]
prompt_text = build_prompt(preset_spec)
print(prompt_text[:300])
```

---

### 💻 Command-Line Interface (CLI)

```bash
# Default execution runs the stdio FastMCP server
promptograph

# Explicit MCP server mode
promptograph mcp

# Launch zero-dependency offline web UI
promptograph web 8765

# Full-text search across 20,475 prompts
promptograph search "system prompt cursor"

# Quick heuristic audit of a prompt string
promptograph validate "You are a code reviewer. Do not explain syntax."

# Display corpus statistics
promptograph stats
```

---

### 🌐 Offline Web Dashboard

Promptograph contains a complete, zero-dependency local web dashboard written in vanilla HTML/JS and Python stdlib:
* **Prompts Explorer:** Search, filter, and inspect raw prompt text with token counts.
* **Side-by-Side Diff:** Color-coded unified diff between model prompts (e.g., Claude 3.5 vs Claude 4, ChatGPT 4o vs o3).
* **Heuristic Audit Lab:** Interactive score breakdown with actionable suggestions.
* **Curated Skills Hub:** Interactive browser for all 226 skills across 37 categories with 1-click blueprint copying.

Run locally:
```bash
promptograph web 8765
```
Or view the static interface on GitHub Pages: [https://4pixeltechBR.github.io/promptograph/](https://4pixeltechBR.github.io/promptograph/)

---

### 📊 Verified Metrics & Breakdown

| Metric | Official Count | Source / Notes |
|---|---|---|
| **Indexed System Prompts** | **20,475** | Sourced from 55 public GitHub repos & 6 HuggingFace datasets |
| **Curated Skills** | **226+** | Operational blueprints with code, guidelines, and tool schemas |
| **Skill Domains** | **37 categories** | Elite Software, Audio, Video, SRE, Quant, OSINT, Local LPs, etc. |
| **FastMCP Tools** | **7 tools** | 4 for prompt engineering + 3 for skills dynamic retrieval |
| **Tokens Indexed** | **~94,000,000** | Full corpus parsed and normalized |
| **Words Indexed** | **70.5M words** | Real-world production instructions (2022–2026) |
| **Top AI Labs Represented** | **40+ labs** | OpenAI (7.7k), DeepSeek (6.8k), Anthropic (1.8k), Google, xAI, Meta, Cursor |
| **Package Size (PyPI Wheel)** | **~679 KB** | Compressed wheel containing prompts index + skills manifest |
| **Runtime Memory (RAM)** | **~50 MB** | Lightweight Python stdlib execution |

---

### 🏗️ Architecture & Package Structure

```
promptograph/
├── pyproject.toml                     # Modern PEP 621 packaging (hatchling)
├── server.py                          # Standalone stdlib HTTP server
├── scripts/
│   ├── promptograph_mcp_server.py     # Standalone MCP stdio server
│   ├── search_promptograph.py         # Standalone CLI search & stats tool
│   └── test_promptograph_mcp.py       # Comprehensive 7-tool test suite
├── src/
│   ├── promptograph/                  # PyPI package core
│   │   ├── __init__.py                # Version 0.3.2, public API exports
│   │   ├── cli.py                     # Unified entrypoint (mcp/web/search/stats/validate)
│   │   ├── mcp_server.py              # Native FastMCP server with resilient imports
│   │   ├── validator.py               # 13 heuristic rules + 6 red flags
│   │   ├── builder.py                 # 5 production synthesis presets
│   │   ├── skills_registry.py         # Dynamic resolver for 226 curated skills
│   │   ├── data/                      # Embedded indexes (index_filtered.json, skills_manifest.json)
│   │   └── static/                    # Embedded offline web UI (app.js, index.html)
│   └── skills/promptograph/           # Backward-compatible import wrappers
├── data/
│   ├── index_filtered.json            # Unified dataset of 20,475 production prompts
│   └── promptograph/
│       └── skills_manifest.json       # Curated registry of 226 skills in 37 domains
├── static/                            # Web UI assets (HTML5, Tailwind, Vanilla JS)
├── CHANGELOG.md                       # Complete release history
├── LICENSE                            # MIT License
└── README.md                          # Bilingual documentation
```

---

### 📜 License, Attribution & Ethics

* **License:** MIT License — see [LICENSE](LICENSE).
* **Attributions:** All indexed prompts belong to their respective creators, labs, and open-source curators. See [ATTRIBUTIONS.md](ATTRIBUTIONS.md).
* **Ethical Boundary:** Promptograph is designed strictly for research, educational transparency, prompt auditability, and empowering legitimate software engineering agents. Do not use it to craft malicious jailbreaks, bypass safety filters, or violate provider Terms of Service.
* **Maintainer:** [@4pixeltechBR](https://github.com/4pixeltechBR) — 4Pixel Tech.

---

## 🇧🇷 Português

### O que é o Promptograph?

O **Promptograph** é um toolkit profissional que acaba com o "chutômetro" na engenharia de prompts e equipa agentes de IA com habilidades técnicas operacionais prontas para uso.

Ele resolve três gargalos fundamentais do ecossistema de inteligência artificial:
1. **O Fim da Adivinhação:** A maioria dos desenvolvedores interage com modelos como caixas-pretas. O Promptograph entrega uma biblioteca pesquisável com **20.475 system prompts reais de produção** extraídos de 55 repositórios públicos (incluindo Anthropic, OpenAI, Google, Cursor, xAI, Meta, DeepSeek, Perplexity e Cognition).
2. **Auditoria de Qualidade e Segurança:** Como saber se as instruções do seu assistente são seguras e completas antes de ir para produção? O **validador heurístico determinístico** do Promptograph avalia seu prompt contra 13 boas práticas comprovadas e 6 alertas vermelhos (nota de 0 a 100%, conceitos A+ a F).
3. **Cinto de Utilidades para Agentes de Código:** Agentes autônomos (Claude Desktop, Cursor, Windsurf, Claude Code, Antigravity) frequentemente têm "amnésia" técnica de domínio. O Promptograph funciona como um **Servidor FastMCP** plugável com **226 skills curadas** em 37 categorias de engenharia que o agente consulta e executa em tempo real.

---

### ⚡ Início Rápido em 10 Segundos

O Promptograph está publicado no **PyPI** e pode ser executado com **zero instalação** via `uvx`:

#### 1. Busca Instantânea via Terminal (Sem clonar repositório)
```bash
# Buscar nos 20.475 prompts reais de produção
uvx promptograph search "claude coding"

# Validar a qualidade de um prompt contra 13 regras
uvx promptograph validate "Você é um assistente de código. Seja direto e objetivo."

# Exibir estatísticas completas e distribuição de laboratórios
uvx promptograph stats
```

#### 2. Iniciar Dashboard Web Local
```bash
uvx promptograph web 8765
# Acesse http://localhost:8765 no seu navegador
```

#### 3. Instalação via Pip / UV
```bash
pip install promptograph
# Ou com o uv:
uv add promptograph
```

---

### 🔌 Servidor FastMCP para Agentes de IA

O Promptograph implementa nativamente o **Model Context Protocol (MCP)** usando `FastMCP` sobre `stdio`. Ele conecta instantaneamente ao **Claude Desktop**, **Cursor**, **Windsurf**, **Claude Code** e **Antigravity**.

#### Configuração MCP Zero-Install (Recomendada)
Basta adicionar este bloco ao arquivo de configuração MCP do seu aplicativo (`claude_desktop_config.json`, `.cursor/mcp.json`, etc.):

```json
{
  "mcpServers": {
    "promptograph": {
      "command": "uvx",
      "args": ["promptograph"]
    }
  }
}
```

#### Configuração via Clone Local (Alternativa)
Se você clonou o repositório localmente:
```json
{
  "mcpServers": {
    "promptograph": {
      "command": "python",
      "args": ["/caminho/para/promptograph/scripts/promptograph_mcp_server.py"]
    }
  }
}
```

---

### 🛠️ As 7 Ferramentas MCP Explicadas

Assim que conectado via MCP, o seu assistente de IA ganha 7 ferramentas nativas:

| Ferramenta | Categoria | Parâmetros | O que ela faz |
|---|---|---|---|
| `promptograph_search` | Prompts | `query`, `company`, `model`, `limit` | Busca em 20.475 prompts de produção por empresa, modelo ou palavra-chave |
| `promptograph_validate` | Qualidade | `content` | Avalia o prompt (0–100%, Nota A+ a F) checando 13 regras estruturais e 6 red flags |
| `promptograph_generate` | Síntese | `preset_name`, `spec_json` | Gera prompts completos baseados em presets validados (Claude, GPT, Cursor, Devin) |
| `promptograph_stats` | Métricas | — | Retorna contagens de tokens, distribuição de empresas e modelos do acervo |
| `promptograph_skills_search` | Skills | `query`, `category`, `limit` | Pesquisa entre 226+ blueprints operacionais em 37 domínios técnicos |
| `promptograph_skills_get` | Skills | `skill_id` | Recupera o manual executável completo (`SKILL.md`) com códigos para o agente rodar |
| `promptograph_skills_categories`| Skills | — | Lista todas as 37 categorias técnicas com a quantidade de skills em cada uma |

#### Exemplos de comandos para dar ao seu agente:
* *"Pesquise no Promptograph como o Claude define regras para escrever código limpo."*
* *"Valide este system prompt que escrevi antes de eu colocar no bot de atendimento."*
* *"Busque uma skill de normalização de áudio no Promptograph e aplique o código no meu projeto."*

---

### 🐍 Uso como Biblioteca Python

Você pode importar o Promptograph diretamente no código do seu projeto ou agente Python, sem overhead de servidor:

```python
from promptograph import (
    validate_prompt,
    build_prompt,
    search_skills,
    get_skill_blueprint,
    get_skills_stats,
    PRESET_TEMPLATES,
)

# 1. Auditar um prompt de sistema programaticamente
relatorio = validate_prompt("Você é um tutor de Python. Explique conceitos com exemplos.")
print(f"Nota: {relatorio['grade']} ({relatorio['score']}%)")
print(f"Regras aprovadas: {len(relatorio['passed'])}/13")

# 2. Descobrir e carregar skills operacionais
resultados = search_skills(query="clean-code")
if resultados:
    skill = get_skill_blueprint(resultados[0]["id"])
    print(f"Skill carregada: {skill['name']} [{skill['category']}]")
    print(skill["blueprint"][:400])  # Markdown com instruções e código executável

# 3. Gerar prompt profissional a partir de presets
spec_preset = PRESET_TEMPLATES["claude_coding_agent"]["spec"]
prompt_gerado = build_prompt(spec_preset)
print(prompt_gerado[:300])
```

---

### 💻 Interface de Linha de Comando (CLI)

```bash
# Execução padrão inicia o servidor MCP stdio (usado pelo uvx)
promptograph

# Modo explícito de servidor FastMCP
promptograph mcp

# Inicia a interface web offline zero-dependency
promptograph web 8765

# Busca rápida de texto em 20.475 prompts
promptograph search "system prompt cursor"

# Validação rápida de um texto de prompt
promptograph validate "Você é um assistente de suporte. Responda educadamente."

# Exibe estatísticas globais do acervo
promptograph stats
```

---

### 🌐 Dashboard Web Offline

O Promptograph inclui uma interface gráfica local completa em HTML5/JS puro e Python stdlib:
* **Explorador de Prompts:** Busca instantânea, filtros por lab e visualização de tokens e personas.
* **Diff Comparativo Lado a Lado:** Comparador visual com destaque de alterações (verde/vermelho) entre versões de prompts.
* **Laboratório de Auditoria Heurística:** Avaliação interativa em tempo real com sugestões práticas de correção.
* **Catálogo Visual de Skills MCP:** Navegação pelas 226 skills em 37 categorias com cópia de blueprints em 1 clique.

Para rodar localmente:
```bash
promptograph web 8765
```
Ou acesse a versão online no GitHub Pages: [https://4pixeltechBR.github.io/promptograph/](https://4pixeltechBR.github.io/promptograph/)

---

### 📊 Estatísticas Oficiais & Distribuição

| Métrica | Contagem Oficial | Detalhes |
|---|---|---|
| **Prompts Indexados** | **20.475** | Extraídos de 55 repositórios GitHub e 6 datasets do HuggingFace |
| **Skills Curadas** | **226+** | Blueprints operacionais com código executável e diretrizes |
| **Categorias de Skills** | **37 domínios** | Engenharia de Software, Áudio, Vídeo, SRE, Quant, OSINT, LPs, etc. |
| **Ferramentas FastMCP** | **7 ferramentas** | 4 dedicadas a prompts + 3 dedicadas a skills de agentes |
| **Tokens Indexados** | **~94.000.000** | Corpus completo auditado e normalizado |
| **Palavras Indexadas** | **70,5M palavras** | Instruções de produção reais de 2022 a 2026 |
| **Principais Laboratórios** | **40+ empresas** | OpenAI (7.7k), DeepSeek (6.8k), Anthropic (1.8k), Google, xAI, Meta, Cursor |
| **Tamanho do Pacote (Wheel PyPI)** | **~679 KB** | Pacote comprimido contendo índice e manifesto de skills |
| **Consumo de Memória (RAM)** | **~50 MB** | Execução leve em Python padrão sem dependências pesadas |

---

### 🏗️ Arquitetura do Pacote

```
promptograph/
├── pyproject.toml                     # Configuração de build moderna PEP 621 (hatchling)
├── server.py                          # Servidor HTTP standalone Python stdlib
├── scripts/
│   ├── promptograph_mcp_server.py     # Servidor FastMCP standalone
│   ├── search_promptograph.py         # CLI standalone de busca e estatísticas
│   └── test_promptograph_mcp.py       # Suíte completa de testes das 7 ferramentas
├── src/
│   ├── promptograph/                  # Núcleo do pacote PyPI
│   │   ├── __init__.py                # Versão 0.3.2 e exports da API pública
│   │   ├── cli.py                     # Entrypoint unificado (mcp/web/search/stats/validate)
│   │   ├── mcp_server.py              # Servidor FastMCP com importações resilientes
│   │   ├── validator.py               # 13 regras heurísticas + 6 red flags
│   │   ├── builder.py                 # 5 presets de produção
│   │   ├── skills_registry.py         # Registro e busca das 226 skills curadas
│   │   ├── data/                      # Índices embutidos (index_filtered.json, skills_manifest.json)
│   │   └── static/                    # UI web embutida (app.js, index.html)
│   └── skills/promptograph/           # Wrappers de retrocompatibilidade
├── data/
│   ├── index_filtered.json            # Dataset unificado de 20.475 prompts reais
│   └── promptograph/
│       └── skills_manifest.json       # Manifesto curado de 226 skills em 37 domínios
├── static/                            # Arquivos do frontend (HTML5, Tailwind, Vanilla JS)
├── CHANGELOG.md                       # Histórico completo de releases
├── LICENSE                            # Licença MIT
└── README.md                          # Documentação bilíngue oficial
```

---

### 📜 Licença, Atribuição e Ética

* **Licença:** MIT License — veja [LICENSE](LICENSE).
* **Atribuição:** Todos os prompts indexados pertencem aos seus respectivos autores, laboratórios e curadores da comunidade open source. Veja [ATTRIBUTIONS.md](ATTRIBUTIONS.md).
* **Uso Ético:** O Promptograph foi concebido para pesquisa, transparência, educação técnica e expansão legítima de agentes autônomos de engenharia. É expressamente proibido usá-lo para desenhar ataques maliciosos, contornar travas de segurança ou violar Termos de Serviço de provedores de IA.
* **Maintainer:** [@4pixeltechBR](https://github.com/4pixeltechBR) — 4Pixel Tech.
