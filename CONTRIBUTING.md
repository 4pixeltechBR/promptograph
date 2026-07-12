# Contributing to Meta-Prompt Engine

Thank you for considering a contribution! This project exists because of the
open-source community, and we welcome help in any form.

## Quick Links

- 🐛 [Report a bug](https://github.com/YOUR_USER/meta-prompt-engine/issues/new?template=bug.md)
- 💡 [Request a feature](https://github.com/YOUR_USER/meta-prompt-engine/issues/new?template=feature.md)
- 🔧 [Submit a pull request](https://github.com/YOUR_USER/meta-prompt-engine/pulls)
- 💬 [Discussions](https://github.com/YOUR_USER/meta-prompt-engine/discussions)

## How to Contribute

### 🐛 Reporting Bugs

Open an issue with:
- **Title**: short, descriptive
- **Steps to reproduce**: minimum code/config
- **Expected behavior**
- **Actual behavior**
- **Environment**: OS, Python version, browser (if UI)
- **Logs/screenshots** if applicable

### 💡 Suggesting Features

Open an issue with:
- **Use case**: what problem does this solve?
- **Proposed solution**: how would it work?
- **Alternatives considered**: what else did you think about?

### 🔧 Pull Requests

1. **Fork** the repo
2. **Create a branch**: `git checkout -b feature/my-feature`
3. **Make your changes**
4. **Test locally**: `python3 server.py 8765` and click around
5. **Run the validator on your code** (if it touches validators/)
6. **Commit**: use [Conventional Commits](https://www.conventionalcommits.org/)
   (`feat:`, `fix:`, `docs:`, `chore:`)
7. **Push** and open a PR

## Areas Where We Need Help

### 🆕 Adding New Presets

The 5 current presets cover the biggest tools. We want more:
- **Notion AI** style
- **Discord Clyde** style
- **Windsurf** style
- **Replit** style
- **Lovable** style
- **Aider** style
- **Continue.dev** style
- **Zed AI** style

To add a preset:
1. Find the equivalent prompt in the index
2. Copy its structure
3. Add to `PRESET_TEMPLATES` in `generator/builder.py`
4. Add a button in `renderGenerate()` in `static/app.js`
5. Test by generating and validating

### 🔍 Improving the Validator

The validator has 13 checks. We want more. Ideas:
- Check for `examples` with `good_response` AND `bad_response` (Anthropic
  pattern)
- Detect missing `<important>` or `<critical>` sections
- Warn if the prompt has the same word repeated 50+ times
- Score based on structural complexity (XML tag count, section count)

### 🌐 Adding New Source Repos

1. Find a GitHub repo with system prompts
2. Add to the index by running parser on it
3. Update the prompt count in README

### 🌍 Translations

- UI translations (Spanish, French, Japanese, Chinese)
- README translations to other languages

### 🐛 Bug Fixes

Check the [issues](https://github.com/YOUR_USER/meta-prompt-engine/issues)
for open bugs.

## Code Style

- **Python**: PEP 8, 4-space indents, snake_case
- **JavaScript**: modern ES6+, 2-space indents, camelCase
- **HTML/CSS**: 2-space indents, kebab-case classes
- **No frameworks** unless absolutely necessary (we're keeping it stdlib)

## Testing

There's no formal test suite yet. Before submitting:

```bash
# Smoke test
python3 server.py 8765 &
sleep 2
curl http://localhost:8765/api/stats
curl -X POST http://localhost:8765/api/validate \
  -H "Content-Type: application/json" \
  -d '{"content": "You are a test assistant."}'
kill %1
```

## Community

- Be respectful and inclusive
- Assume good faith
- No harassment, discrimination, or personal attacks
- We're all here to learn

## License

By contributing, you agree that your contributions will be licensed under
the MIT License.
