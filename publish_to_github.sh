#!/usr/bin/env bash
# publish_to_github.sh — Publica o Promptograph no GitHub
# Requer: GH_TOKEN (Personal Access Token com scope 'repo')
#
# Uso:
#   export GH_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
#   ./publish_to_github.sh

set -e

REPO_NAME="${REPO_NAME:-promptograph}"
REPO_DESC="${REPO_DESC:-Browse, diff, validate and generate AI system prompts, built on 5,300+ real prompts from Claude, ChatGPT, Gemini, Grok, Perplexity, Cursor, Devin and more}"
REPO_PRIVATE="${REPO_PRIVATE:-false}"
GH_USER="${GH_USER:-4pixeltechBR}"

if [ -z "$GH_TOKEN" ]; then
    echo "❌ GH_TOKEN não definido"
    echo ""
    echo "Gere um token em https://github.com/settings/tokens (scope: repo)"
    echo "Depois defina:"
    echo "  export GH_TOKEN=\"ghp_xxxxxxxxxxxxxxxxxxxx\""
    echo "  ./publish_to_github.sh"
    exit 1
fi

echo "🚀 Publicando $REPO_NAME no GitHub"
echo "   Usuário: $GH_USER"
echo "   Privado: $REPO_PRIVATE"
echo ""

# Verifica/cria o repo via API
echo "📦 Criando/verificando repositório..."
curl -s -X POST -H "Authorization: token $GH_TOKEN" \
    -H "Accept: application/vnd.github+json" \
    https://api.github.com/user/repos \
    -d "{\"name\":\"$REPO_NAME\",\"description\":\"$REPO_DESC\",\"private\":$REPO_PRIVATE,\"has_issues\":true,\"has_projects\":true,\"has_wiki\":false}" \
    -o /tmp/repo_create.json
CREATE_STATUS=$(python3 -c "import json; d=json.load(open('/tmp/repo_create.json')); print(d.get('full_name', d.get('message','error')))")
echo "   Repo: $CREATE_STATUS"

# Init git local se necessário
cd /workspace/promptograph
if [ -d .git ]; then
    echo "   Repo local já tem .git, usando existente"
else
    echo "🔧 Inicializando git local..."
    git init -q
    git config user.name "$GH_USER"
    git config user.email "$GH_USER@users.noreply.github.com"
    git branch -M main
    git add .
    git commit -q -m "feat: initial release of Promptograph

- 5,317 system prompts indexed from 20 public GitHub repos
- Browse, Diff, Validate, Generate features
- 5 presets: Claude Code, ChatGPT, Cursor, Perplexity, Devin
- 13 best practices + 6 red flags in validator
- Web UI in vanilla HTML/JS (no build step)
- Python stdlib HTTP server (zero dependencies)
- Docker + GitHub Pages support
- Bilingual README (EN/PT-BR)
- MIT License"
fi

# Push
echo "⬆️  Fazendo push..."
git remote remove origin 2>/dev/null || true
git remote add origin "https://$GH_TOKEN@github.com/$GH_USER/$REPO_NAME.git"
git push -u origin main 2>&1 | tail -10

echo ""
echo "✅ Pronto!"
echo "   https://github.com/$GH_USER/$REPO_NAME"
echo ""
echo "Próximos passos:"
echo "  1. Settings → General → Topics: ai, prompt-engineering, llm, claude, chatgpt, system-prompts, open-source, prompt-toolkit"
echo "  2. Settings → Pages → Source: GitHub Actions (ativa GitHub Pages pra UI online)"
echo "  3. Crie a primeira release: git tag v0.1.0 && git push --tags"
echo "  4. Compartilhe no Twitter/LinkedIn com a hashtag #promptengineer ou #llm"
