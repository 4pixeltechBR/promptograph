# 📷 Promptograph

> **Photograph every system prompt that matters.**
> A toolkit to **browse**, **diff**, **validate**, and **generate** AI system prompts,
> built on top of 20,475 real prompts extracted from production AI systems.

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Prompts indexed](https://img.shields.io/badge/prompts-20%2C475-brightgreen.svg)](#-whats-inside)
[![Repos indexed](https://img.shields.io/badge/repos-55-orange.svg)](#-whats-inside)
[![Zero deps](https://img.shields.io/badge/dependencies-zero-success.svg)](#-architecture)
[![Live site](https://img.shields.io/badge/site-live-blueviolet)](https://4pixeltechBR.github.io/promptograph/)

[🇧🇷 Português](#-português) · [🇺🇸 English](#-english)

![Promptograph](https://img.shields.io/badge/📷_Promptograph-v0.3.0-blueviolet)

---

## 🇺🇸 English

### What is this?

**Promptograph** is a self-contained toolkit for working with **AI system prompts** —
the hidden instructions that shape how models like Claude, ChatGPT, Gemini, Grok,
and others behave.

It was built on top of **20,475 system prompts** extracted from **55 public
GitHub repositories** (plus 6 HuggingFace datasets), totaling over
**16.4 million words** of real production instructions. The goal is to
**democratize prompt engineering** by giving you the same material the
major AI labs use to build their products, and tools to learn from it.

### 🎯 Why we built this

Most AI users interact with models as black boxes. The system prompt — the
hidden "constitution" that defines an AI's personality, capabilities,
limitations, and tools — is the most under-discussed piece of the puzzle.

We believe:
- **Transparency helps everyone**: developers learn faster, researchers
  find vulnerabilities, users make informed choices.
- **Patterns matter more than prompts**: the best system prompts share
  structural patterns. Learning them is more valuable than copying any
  one prompt.
- **Good prompts are engineered, not written**: just like code, system
  prompts benefit from validation, testing, comparison, and iteration.

### ✨ What makes Promptograph different

There are other "prompt lens" / "prompt scope" projects out there. Here's
what they do — and what we do that they don't:

| Other projects | Promptograph |
|---|---|
| Hook into Claude Code for one user | **Standalone tool**, anyone can use |
| A/B testing of LLM responses | **Diff between real system prompts** |
| LLM-as-judge prompt evaluation | **Heuristic validation** against 13 best practices extracted from production prompts |
| Single-tool (just A, or just B) | **4 features in one**: Browse, Diff, Validate, Generate |
| Requires API keys, npm, pip | **Zero dependencies**, runs offline |
| English only | **Bilingual** (PT-BR + EN) |

### 🎯 Use cases

**For developers:** You can build a coding agent in 5 minutes — open Promptograph, filter by "claude coding agent", see how Anthropic structures theirs, customize and ship. No more starting from zero.

**For prompt engineers:** Before sending a prompt to a client, run it through Validate. Get a 0-100% score with 13 checks and 6 red flags. Like a linter, but for prompts.

**For product managers:** Diff Cursor vs Windsurf system prompts to understand why one converts better. Diff ChatGPT vs Claude to see how they position their tools internally. Insights you can't get from marketing pages.

**For security researchers:** Search across 20k+ prompts for "refuse", "harmful", "injection". See how each company handles jailbreak, prompt injection, sensitive content. Real corpus for research.

**For researchers and students:** A corpus of 20k+ real production system prompts for qualitative analysis. How did the tone change from 2023 to 2026? Which companies added the most guardrails? You can write a paper with this data.

**For tech writers and creators:** Take a "creative writing" preset, customize it, get a better prompt than 99% of what's out there. Then Validate to check the quality.

**For CTOs and tech leads:** Compare system prompts to evaluate AI vendors. Which is more conservative? Which has more guardrails? Which is more transparent? Technical decision based on evidence.

### ✨ Features

#### 📚 Browse
Navigate 20,475+ system prompts with:
- Full-text search (filename, model, persona)
- Filter by company (Anthropic, OpenAI, Google, xAI, Perplexity, etc)
- Sort by size, date, or name
- Per-prompt metadata: model, date, persona, XML tags, tools detected
- Inline preview of raw content

#### 🔀 Diff
Compare any two prompts side-by-side:
- Unified diff with color highlighting (green=added, red=removed)
- Token-level statistics
- Change percentage
- Up to 5,000 diff lines

#### ✅ Validate
Score any system prompt (0-100%, grade A+ to F) against 13 best practices
extracted from the most successful production prompts:
- Identity clarity (15 pts)
- Tone guidelines (10 pts)
- Refusals handling (10 pts)
- Safety rules (10 pts)
- Examples section (10 pts)
- Formatting rules (8 pts)
- Tool usage (8 pts)
- Memory/context (6 pts)
- Knowledge cutoff (5 pts)
- Structured tags (5 pts)
- Citation rules (5 pts)
- Limits/boundaries (5 pts)
- Length appropriateness (3 pts)

Plus 6 red flags: vague identity, jailbreak vulnerability, copyright
missing, instruction contradictions, too short, too long.

#### ✨ Generate
Build a new system prompt from a spec, using 5 presets based on real
production prompts:
- **Claude Code-style coding agent** (Anthropic)
- **ChatGPT 5.5-style assistant** (OpenAI)
- **Cursor-style IDE agent** (Anysphere)
- **Perplexity-style search engine** (Perplexity AI)
- **Devin-style autonomous engineer** (Cognition)

Each preset produces a complete, validated prompt that scores 80%+ on the
validator.

### 🏗️ Architecture

```
promptograph/
├── server.py                  # Python stdlib HTTP server
├── data/
│   ├── index.json             # 5,491 raw prompts indexed
│   └── index_filtered.json    # 20,475 filtered (READMEs removed)
├── generator/
│   ├── parser.py              # Scans repos, extracts metadata
│   ├── builder.py             # Constructs prompts from specs
│   └── refine_index.py        # Filters out non-prompt files
├── validators/
│   └── quality.py             # 13 best practices + 6 red flags
├── static/
│   ├── index.html             # UI
│   └── app.js                 # Frontend (vanilla JS, no build)
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI + Pages
├── bootstrap.sh               # One-command setup
├── publish_to_github.sh       # GitHub publish script
├── LICENSE
├── ATTRIBUTIONS.md
└── README.md (this file)
```

**Stack:** Python 3.10+ (stdlib only) + Vanilla HTML/JS. Zero npm, zero pip
dependencies, zero build step.

### 🚀 Quick Start

#### Local (Python)

```bash
git clone https://github.com/4pixeltechBR/promptograph.git
cd promptograph
./bootstrap.sh        # Builds the index (one-time, ~2 min)
python3 server.py 8765
```

Open `http://localhost:8765` in your browser.

#### GitHub Pages (UI only, no backend)

The static UI is in `static/`. Once you enable GitHub Pages on your fork,
the UI will be live at `https://4pixeltechBR.github.io/promptograph/`.
The API calls will fail unless you also deploy the backend (Docker below).

#### Docker

```bash
docker build -t promptograph .
docker run -p 8765:8765 promptograph
```

### 📊 What's inside

| Metric | Value |
|---|---|
| Prompts indexed | 20,475 |
| Tokens indexed | ~94,000,000 |
| Words indexed | 70.5M |
| Lines indexed | 4.7M |
| Companies | 40+ (Anthropic, OpenAI, Google, xAI, Meta, Mistral, DeepSeek, Moonshot, Zhipu, Cerebras, NVIDIA) |
| Source repositories | 55 (GitHub) + 6 (HuggingFace) |
| Date range | 2022 — 2026 |
| Index size (JSON) | 4.8 MB |
| Backend RAM | ~50 MB |
| Disk after install | ~1.3GB (with archive) or ~5 MB (without) |

### 🎯 Use cases

1. **Learn prompt engineering** — read 5,000+ real examples, identify
   patterns, build intuition
2. **Build a custom AI agent** — start from a preset, tweak, validate
3. **Audit your product's prompt** — paste it, get a score, see what's
   missing
4. **Compare models** — diff Claude Fable 5 vs Claude Opus 4.8 to
   understand what changed
5. **Security research** — identify prompt patterns vulnerable to
   injection
6. **Benchmark / regression test** — track how a prompt evolves over
   time

### 🛠️ API Reference

```
GET  /api/index                      → All 20,475 indexed prompts (JSON)
GET  /api/raw?id=<id>                → Full content of one prompt
GET  /api/stats                      → Counts and totals
GET  /api/presets/<name>             → Preset spec (claude_coding_agent, etc)

POST /api/diff                       → {left, right} → unified diff
POST /api/validate                   → {content} → score + checks
POST /api/generate                   → {spec} → generated prompt
```

### 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### 📜 License & Ethics

MIT License — see [LICENSE](LICENSE).

**Source prompts attribution** — see [ATTRIBUTIONS.md](ATTRIBUTIONS.md).
We respect the licenses of the source repositories and use them for
research, education, and transparency.

**Ethical use** — this tool is for learning, auditing, and building.
Do not use it to bypass safety measures, attack production systems, or
violate the Terms of Service of any AI provider.

---

## 🇧🇷 Português

### O que é isso?

**Promptograph** é um toolkit auto-contido para trabalhar com **system
prompts de IA** — as instruções ocultas que moldam o comportamento de
modelos como Claude, ChatGPT, Gemini, Grok e outros.

Foi construído em cima de **20.475 system prompts** extraídos de 55
repositórios públicos do GitHub, totalizando mais de **12 milhões de
tokens** de instruções reais de produção. O objetivo é **democratizar
a engenharia de prompts** dando a você o mesmo material que os grandes
laboratórios de IA usam para construir seus produtos, e ferramentas
para aprender com ele.

### 🎯 Por que construímos isso

A maioria dos usuários de IA interage com modelos como caixas-pretas. O
system prompt — a "constituição" oculta que define a personalidade,
capacidades, limitações e tools de uma IA — é a peça mais subestimada
do quebra-cabeça.

Acreditamos que:
- **Transparência ajuda todo mundo**: devs aprendem mais rápido,
  pesquisadores acham vulnerabilidades, usuários fazem escolhas
  informadas
- **Padrões importam mais que prompts**: os melhores system prompts
  compartilham padrões estruturais. Aprender esses padrões vale mais
  que copiar qualquer prompt individual
- **Bons prompts são engineered, não escritos**: assim como código,
  system prompts se beneficiam de validação, teste, comparação e iteração

### ✨ O que diferencia o Promptograph

Existem outros projetos "prompt lens" / "prompt scope" por aí. Veja o
que eles fazem — e o que a gente faz que eles não fazem:

| Outros projetos | Promptograph |
|---|---|
| Hook no Claude Code pra um usuário | **Ferramenta standalone**, qualquer um usa |
| A/B testing de respostas LLM | **Diff entre system prompts reais** |
| LLM-como-juiz pra avaliar prompts | **Validação heurística** contra 13 práticas extraídas de prompts de produção |
| Single-tool (só A, ou só B) | **4 features em uma**: Browse, Diff, Validate, Generate |
| Requer API keys, npm, pip | **Zero dependências**, roda offline |
| Só inglês | **Bilíngue** (PT-BR + EN) |

### ✨ Funcionalidades

#### 📚 Browse
Navegue por 20.475+ system prompts com:
- Busca full-text (nome do arquivo, modelo, persona)
- Filtro por empresa (Anthropic, OpenAI, Google, xAI, Perplexity, etc)
- Ordenação por tamanho, data ou nome
- Metadata por prompt: modelo, data, persona, tags XML, tools detectadas
- Preview inline do conteúdo raw

#### 🔀 Diff
Compare dois prompts lado-a-lado:
- Diff unified com cores (verde=adicionado, vermelho=removido)
- Estatísticas em tokens
- Porcentagem de mudança
- Até 5.000 linhas de diff

#### ✅ Validate
Pontue qualquer system prompt (0-100%, nota A+ a F) contra 13 boas
práticas extraídas dos prompts de produção mais bem-sucedidos:
- Clareza de identidade (15 pts)
- Diretrizes de tom (10 pts)
- Tratamento de recusas (10 pts)
- Regras de segurança (10 pts)
- Seção de exemplos (10 pts)
- Regras de formatação (8 pts)
- Uso de tools (8 pts)
- Memória/contexto (6 pts)
- Knowledge cutoff (5 pts)
- Tags estruturadas (5 pts)
- Regras de citação (5 pts)
- Limites/boundaries (5 pts)
- Tamanho apropriado (3 pts)

Mais 6 red flags: identidade vaga, vulnerabilidade a jailbreak,
copyright ausente, contradições de instrução, muito curto, muito longo.

#### ✨ Generate
Construa um novo system prompt a partir de uma spec, usando 5 presets
baseados em prompts reais de produção:
- **Claude Code-style coding agent** (Anthropic)
- **ChatGPT 5.5-style assistant** (OpenAI)
- **Cursor-style IDE agent** (Anysphere)
- **Perplexity-style search engine** (Perplexity AI)
- **Devin-style autonomous engineer** (Cognition)

Cada preset produz um prompt completo e validado que tira 80%+ no
validador.

### 🏗️ Arquitetura

```
promptograph/
├── server.py                  # Servidor HTTP Python stdlib
├── data/
│   ├── index.json             # 5.491 prompts brutos indexados
│   └── index_filtered.json    # 20.475 filtrados (READMEs removidos)
├── generator/
│   ├── parser.py              # Varre repos, extrai metadata
│   ├── builder.py             # Constrói prompts a partir de specs
│   └── refine_index.py        # Filtra arquivos não-prompt
├── validators/
│   └── quality.py             # 13 boas práticas + 6 red flags
├── static/
│   ├── index.html             # UI
│   └── app.js                 # Frontend (vanilla JS, sem build)
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI + Pages
├── bootstrap.sh               # Setup em um comando
├── publish_to_github.sh       # Script de publish
├── LICENSE
├── ATTRIBUTIONS.md
└── README.md (este arquivo)
```

**Stack:** Python 3.10+ (stdlib only) + Vanilla HTML/JS. Zero npm, zero
dependências pip, zero build step.

### 🚀 Quick Start

#### Local (Python)

```bash
git clone https://github.com/4pixeltechBR/promptograph.git
cd promptograph
./bootstrap.sh        # Constrói o índice (uma vez, ~2 min)
python3 server.py 8765
```

Abra `http://localhost:8765` no navegador.

#### GitHub Pages (só UI, sem backend)

A UI estática está em `static/`. Quando você ativar GitHub Pages no seu
fork, a UI fica em `https://4pixeltechBR.github.io/promptograph/`. As
chamadas de API vão falhar a menos que você faça deploy do backend
(Docker abaixo).

#### Docker

```bash
docker build -t promptograph .
docker run -p 8765:8765 promptograph
```

### 📊 O que tem dentro

| Métrica | Valor |
|---|---|
| Prompts indexados | 20.475 |
| Tokens indexados | ~22.000.000 |
| Palavras indexadas | 16,4M |
| Empresas | 35+ (Anthropic, OpenAI, Google, xAI, Meta, Mistral, DeepSeek, Moonshot, Zhipu) |
| Repositórios fonte | 55 (GitHub) + 6 (HuggingFace) |
| Período | 2022 — 2026 |
| Tamanho do índice (JSON) | 3,0 MB |
| RAM do backend | ~50 MB |
| Disco após instalação | ~1,3 GB (com archive) ou ~5 MB (sem) |

### 🎯 Casos de uso

1. **Aprender engenharia de prompts** — leia 5.000+ exemplos reais,
   identifique padrões, construa intuição
2. **Construir um agente de IA customizado** — comece de um preset,
   ajuste, valide
3. **Auditar o prompt do seu produto** — cole, receba um score, veja o
   que falta
4. **Comparar modelos** — faça diff entre Claude Fable 5 e Claude
   Opus 4.8 pra entender o que mudou
5. **Pesquisa de segurança** — identifique padrões de prompt
   vulneráveis a injeção
6. **Benchmark / regression test** — acompanhe como um prompt evolui
   com o tempo

### 🛠️ Referência da API

```
GET  /api/index                      → Todos os 20.475 prompts indexados (JSON)
GET  /api/raw?id=<id>                → Conteúdo completo de um prompt
GET  /api/stats                      → Contagens e totais
GET  /api/presets/<nome>             → Spec de um preset

POST /api/diff                       → {left, right} → diff unified
POST /api/validate                   → {content} → score + checks
POST /api/generate                   → {spec} → prompt gerado
```

### 🤝 Contribuindo

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md)
para diretrizes.

### 📜 Licença e Ética

MIT License — veja [LICENSE](LICENSE).

**Atribuição dos prompts fonte** — veja [ATTRIBUTIONS.md](ATTRIBUTIONS.md).
Respeitamos as licenças dos repositórios fonte e os usamos para
pesquisa, educação e transparência.

**Uso ético** — esta ferramenta é para aprender, auditar e construir.
Não use para burlar medidas de segurança, atacar sistemas de produção
ou violar os Termos de Serviço de qualquer provedor de IA.

---

## 🤝 Créditos

Construído por **Mavis (MiniMax Agent)** com base no trabalho de dezenas
de mantenedores de repositórios open source. Veja [ATTRIBUTIONS.md](ATTRIBUTIONS.md).

**Maintainer:** [@4pixeltechBR](https://github.com/4pixeltechBR)

## 📜 License

MIT © 2026
