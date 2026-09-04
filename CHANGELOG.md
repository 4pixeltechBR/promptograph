# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-09-03

### Added — "The Frontier Update"
- **Major archive expansion**: 49 → **55 repos**, 10,483 → **20,475 prompts** (+95%)
- **Archive size**: 802MB → **1.3GB** (+62%)
- **Newly integrated top-tier repos**:
  - **`deepseek-ai/deepseek-harness`** (⭐ 210.9k) — Official DeepSeek agent harness, MIT, "Everything is a Plugin". System prompt + 35 extension packages + 4 modes (standard/PTC/minimal/creative)
  - **`alchaincyf/deepseek-harness-orange-book`** (⭐ 1.2k) — 120-page book with reverse-engineered system prompt + 129-line boot checklist + 3 raw session logs, free PDF/EPUB/HTML
  - **`ultraworkers/claw-code`** (⭐ 195.2k) — Clean-room Rust rewrite of leaked Claude Code, fastest GitHub repo ever to hit 100k stars
  - **`openai/codex`** (⭐ 121.2k) — Official OpenAI Codex CLI
  - **`anthropics/claude-code`** (⭐ 143.9k) — Official Anthropic Claude Code
  - **`bradAGI/awesome-cli-coding-agents`** — Curated list of 30+ CLI coding agents

### Added — System prompt leaks (Aug-Sep 2026)
- **Claude Cowork** (175KB) + dispatch (71KB) — 17/ago
- **Claude Science** (155KB) — 14/ago
- **Claude Design** (142KB) + 53 tools + 22 skills + 10 starters — 23/jul
- **Claude in Chrome** (74KB)
- **Claude Voice Mode**
- **Claude for Word, Excel, PowerPoint** (28KB + 17KB + 6KB)
- **Anthropic Interviewer** (11KB)
- **Anthropic Reminders** (10KB)
- **Grok 4.5** (26/jul) + **Grok 4.6** (12/ago) + **Grok Bot** (21/ago)
- **Gemini 3.7 Flash** (18/ago)
- **Codex GPT-5.6 Sol** (separated) + **Terra/Luna**
- **Muse Code (Meta)** (17/ago)
- **Kimi K2.6** (14/jul) — 1T params
- **ZCode (Z.ai GLM-5.3)** — 391KB combinado (15/ago)
- **Ox Alpha / GLM-5.3-Flash** (20-26/ago) — system prompt leaked

### Stats
- **70.5M words** indexed (4.7M lines, 510MB pure text)
- **40+ companies** represented
- **Date range**: 2022 — Sep 2026

## [0.2.0] - 2026-08-13

### Added
- **Massive archive expansion**: 20 → **49 GitHub repositories**, 5,317 → **10,483 prompts**
- New top-tier repos integrated:
  - `x1xhlol/system-prompts-and-models-of-ai-tools` (⭐ 142k — Cursor, Devin, v0, Windsurf, Manus)
  - `elder-plinius/CL4R1T4S` (⭐ 46k — ChatGPT, Claude, Gemini, Grok)
  - `gsd-build/get-shit-done` (⭐ 64k — meta-prompting)
  - `danielmiessler/Fabric` (⭐ 43k — patterns)
  - `Piebald-AI/claude-code-system-prompts` (⭐ 12k — all 27 Claude Code tools)
  - `jujumilk3/leaked-system-prompts` (⭐ 15k)
  - `dontriskit/awesome-ai-system-prompts` (⭐ 6k)
  - `0xeb/TheBigPromptLibrary` (⭐ 5k)
  - `IsHexx/...chinese` — Chinese mirror of x1xhlol
  - `Eversmile12/leaked-llm-prompts` — **Claude Opus 5** (1,511 lines, 135k chars, leaked day-of-launch)
  - `fattail4477/claw-decode` — 512k-line Claude Code source
  - `zebbern/system_prompts_leaks` — fresh fork
  - `safe049/Prompt-Leak` — prompt leak attacks
  - `sikbbang-study/claude-opus-4.6-system-prompt` — Opus 4.6
  - `alpersamur3/ai-system-prompts` — with verified proofs
  - And 30+ more
- **HuggingFace datasets** integrated:
  - `Naomibas/llm-system-prompts-benchmark` (Apache-2.0)
  - `ChuckMcSneed/various_RP_system_prompts` (24 likes)
  - `MetalZuna/System_Prompts` (MIT)
  - `vicgalle/configurable-system-prompt-multitask` (CC-BY-4.0)
  - `teilomillet/system_prompt` (CC-BY-4.0)
  - `Michael-Kozu/system-prompt-reasoning-traces` (Apache-2.0)
- **New companies** detected: Mistral, Moonshot, DeepSeek, Alibaba, Zhipu, Brave, Discord
- **13.7M words** indexed (1.4M lines, 90.9MB of pure text)
- Updated `index_filtered.json` (2.2 MB, 10,483 clean entries)

### Changed
- README updated to v0.2.0 stats (PT-BR + EN)
- Archive size: 96 MB → **802 MB** (8x)
- Repo count in archive: 20 → 49
- UI: added `v0.2.0` badge, tagline, and live stats
- Fixed CI workflow: smoke test no longer fails on missing `scan_all_repos`
- Improved CONTRIBUTING.md with ethics section
- Updated ATTRIBUTIONS.md with all 49 sources
- Single consolidated `ci.yml` (removed separate `pages.yml`)

### Fixed
- GitHub Actions CI failures (was failing on `generator.parser.scan_all_repos` import)
- Added `.gitignore` entries for `data/index.json` (12MB raw, regenerable)
- Better error message in UI when backend is offline

## [0.1.0] - 2026-07-12

### Added
- **Initial release of Promptograph** (renamed from `meta-prompt-engine`)
- 📚 **Browse** — 5,317 system prompts indexed from 20 public GitHub repos
- 🔀 **Diff** — Compare any two prompts with unified diff + stats
- ✅ **Validate** — Score 0-100% (grade A+ to F) against 13 best practices
- ✨ **Generate** — Build new prompts from 5 presets (Claude Code, ChatGPT, Cursor, Perplexity, Devin)
- **Web UI** in vanilla HTML/JS (no build step)
- **Python stdlib HTTP server** (zero dependencies)
- **Docker** support
- **GitHub Actions CI** with Pages deployment
- **Bilingual README** (English + PT-BR)
- **bootstrap.sh** for one-command setup
- **publish_to_github.sh** for easy deployment
- **MIT License** + **ATTRIBUTIONS.md** for source credits

### Indexed Models
- Anthropic: Claude Fable 5, Mythos 5, Opus 4.5/4.6/4.7/4.8, Sonnet 4.5/4.6/5, Haiku 4.5
- OpenAI: GPT-4.1, 4.5, 4o, 5, 5.3, 5.4, 5.5 (all variants)
- Google: Gemini 2.0, 2.5, 3, 3.1, 3.5, Jules, NotebookLM, Bard
- xAI: Grok 4, 4.1, 4.2, 4.3
- Perplexity, Microsoft Copilot, Notion, Brave, Discord
- 28+ AI coding tools (Cursor, Devin, Windsurf, Lovable, v0, etc)
- 10+ Chinese models (DeepSeek, Kimi, GLM, Qwen, etc)

### Repository
- **Name:** Promptograph
- **Tagline:** "Photograph every system prompt that matters."
- **URL:** https://github.com/4pixeltechBR/promptograph
- **License:** MIT

[0.1.0]: https://github.com/4pixeltechBR/promptograph/releases/tag/v0.1.0
