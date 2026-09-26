# 📷 Promptograph v0.3.1 — "The Agent Intelligence & Skills Release"

**Release date:** 2026-09-25  
**Tagline:** Photograph every system prompt that matters & Equip AI Agents with Curated Skills.

---

## 🎯 Highlights

- 🔌 **Native FastMCP Server:** 7 operational tools over standard I/O (stdio), instantly connecting Claude Desktop, Claude Code, Cursor, Windsurf, and Antigravity to your prompt & skills intelligence.
- 🧩 **Curated Agent Skills Registry:** 226+ operational skills blueprints across 37 engineering, AI, multimedia, and automation domains (`data/skills_manifest.json` ~380 KB).
- 📚 **Frontier Corpus Integration:** Full parity with the 20,475 real-world system prompts and ~94 million tokens index.
- 🛡️ **Strict ToS Compliance & Secret Shielding:** 100% audited against GitHub Acceptable Use Policies; zero leaked tokens, zero attack exploits, zero personal machine paths.
- 🚀 **Zero Heavy Dependencies:** Lightweight Python 3.10+ standard library implementation with FastMCP support.

---

## 🆕 What's New in v0.3.1

### 1. 🔌 FastMCP Server for Autonomous Agents
Agents no longer need to parse raw files. Connect Promptograph directly as an MCP server:

```json
{
  "mcpServers": {
    "promptograph": {
      "command": "python",
      "args": ["scripts/promptograph_mcp_server.py"]
    }
  }
}
```

### 2. 🛠️ The 7-Tool Agent Suite

| Tool | Domain | Purpose |
|---|---|---|
| `promptograph_search` | Prompts | Search 20,475 real prompts by company, model, or textual query |
| `promptograph_validate` | Heuristics | Deterministic 13-rule audit scoring prompts (0-100%, Grade A+ to F) |
| `promptograph_generate` | Synthesis | Generate battle-tested prompts using presets (Claude, GPT, Cursor, Devin) |
| `promptograph_stats` | Metrics | Query corpus metrics, token counts, and laboratory breakdowns |
| `promptograph_skills_search` | Skills | Discover 226+ curated skills across 37 technical domains |
| `promptograph_skills_get` | Skills | Retrieve executable operational blueprints (`SKILL.md`) dynamically |
| `promptograph_skills_categories`| Skills | Get domain breakdown and catalog distributions |

### 3. 🧩 Curated Skills Domains (226+ Blueprints)
Includes operational recipes for:
- **Agents & Multi-Agent Swarms:** Kokoro Realtime Voice, Autonomous Coding Agents, OmniParser GUI
- **Elite Software Engineering:** Clean Code, Architecture Design, Profiling, Refactoring
- **Media & 3D Synthesis:** ComfyUI Production Nodes, Remotion Video Pipelines, 3DGS
- **Quantitative Modeling:** DeFi algorithmic models, signal normalizers, backtesting recipes
- **Web & Local Delivery:** Lumora Studio, Brazilian Local Business LPs, Adaptive Crawlers

---

## 📊 Final Stats (v0.3.1)

| Metric | Value |
|---|---|
| **Prompts indexed** | 20,475 |
| **Curated Skills indexed** | 226+ |
| **Skill Domains** | 37 categories |
| **FastMCP Tools** | 7 active tools |
| **Tokens indexed** | ~94,000,000 |
| **Companies** | 40+ (Anthropic, OpenAI, Google, xAI, Meta, Mistral, DeepSeek) |
| **Backend footprint** | ~50 MB RAM |

---

## 🔗 Links

- 🌐 **Repository:** [https://github.com/4pixeltechBR/promptograph](https://github.com/4pixeltechBR/promptograph)
- 📊 **Live Site:** [https://4pixeltechBR.github.io/promptograph/](https://4pixeltechBR.github.io/promptograph/)
- 📜 **License:** MIT © 2026 4Pixel Tech
