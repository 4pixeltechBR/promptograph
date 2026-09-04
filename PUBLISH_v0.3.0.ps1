# 📷 Publish Promptograph v0.3.0 — "The Frontier Update"
# Rode no PowerShell em E:\Skills\promptograph\promptograph

# 1. Adiciona todos os arquivos modificados
Write-Host "📦 Adicionando arquivos atualizados..." -ForegroundColor Cyan
git add data\index_filtered.json
git add data\index.json
git add static\index.html
git add static\app.js
git add README.md
git add CHANGELOG.md
git add ATTRIBUTIONS.md
git add RELEASE_v0.3.0.md

# 2. Commita
Write-Host "`n💾 Commitando v0.3.0..." -ForegroundColor Cyan
git commit -m "v0.3.0: The Frontier Update — 20,475 prompts, 55 repos, 1.3GB

Major archive expansion since v0.2.0:
- Prompts: 10,483 -> 20,475 (+95%)
- Repos: 49 -> 55
- Words indexed: 13.7M -> 70.5M (+415%)
- Archive: 802MB -> 1.3GB

New official open source integrations:
- deepseek-ai/deepseek-harness (210.9k stars, MIT)
- anthropics/claude-code (143.9k stars, official)
- openai/codex (121.2k stars, official)
- ultraworkers/claw-code (195.2k stars, Rust rewrite)
- alchaincyf/deepseek-harness-orange-book (book)
- bradAGI/awesome-cli-coding-agents (curated)

New system prompt leaks (Aug-Sep 2026):
- Claude Cowork, Science, Design, Chrome, Voice
- Grok 4.5, 4.6, Bot
- Gemini 3.7 Flash
- Codex GPT-5.6 (Sol/Terra/Luna)
- Kimi K2.6 (1T params)
- ZCode / GLM-5.3 (391KB)
- Ox Alpha / GLM-5.3-Flash
- Muse Code (Meta)
- OpenCode, Pi, CommandCode

Security research: CVE-2026-54316, 12537, 21852, 24301, Stolen Thoughts"

# 3. Push
Write-Host "`n🚀 Pushing to GitHub..." -ForegroundColor Cyan
git push origin main

# 4. Cria tag v0.3.0
Write-Host "`n🏷️  Criando tag v0.3.0..." -ForegroundColor Cyan
git tag -a v0.3.0 -m "v0.3.0: The Frontier Update

20,475 prompts, 55 repos, 1.3GB archive.
Official open source from DeepSeek, Anthropic, OpenAI.
See RELEASE_v0.3.0.md for full notes."

git push origin v0.3.0

# 5. Cria release (se gh CLI disponível)
if (Get-Command gh -ErrorAction SilentlyContinue) {
    Write-Host "`n📦 Criando release no GitHub..." -ForegroundColor Cyan
    gh release create v0.3.0 `
        --title "📷 Promptograph v0.3.0 - The Frontier Update" `
        --notes-file RELEASE_v0.3.0.md `
        --latest
}

Write-Host "`n✅ v0.3.0 publicado!" -ForegroundColor Green
Write-Host "🌐 https://github.com/4pixeltechBR/promptograph/releases/tag/v0.3.0" -ForegroundColor Green
Write-Host "📊 https://4pixeltechBR.github.io/promptograph/ (atualiza em ~1 min)" -ForegroundColor Green
