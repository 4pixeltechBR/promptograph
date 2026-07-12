"""
refine_index.py — Filtra o índice bruto pra remover READMEs, CONTRIBUTING, etc.
Foca em arquivos que são realmente system prompts.
"""

import json
import re
from pathlib import Path

INDEX_PATH = Path("/workspace/meta-prompt-engine/data/index.json")

# Padrões de arquivos que NÃO são system prompts
NOT_PROMPT_PATTERNS = [
    re.compile(r"^README", re.IGNORECASE),
    re.compile(r"^CONTRIBUTING", re.IGNORECASE),
    re.compile(r"^LICENSE", re.IGNORECASE),
    re.compile(r"^CHANGELOG", re.IGNORECASE),
    re.compile(r"^SECURITY", re.IGNORECASE),
    re.compile(r"\.github/", re.IGNORECASE),
    re.compile(r"^AUTHORS?", re.IGNORECASE),
    re.compile(r"^CODE_OF_CONDUCT", re.IGNORECASE),
    re.compile(r"^PULL_REQUEST", re.IGNORECASE),
    re.compile(r"\.gitignore$", re.IGNORECASE),
    re.compile(r"^funding", re.IGNORECASE),
]

# Arquivos que PARECEM prompts (heurística leve)
PROMPT_KEYWORDS = re.compile(
    r"(you are|você é|you'?re|system\s*prompt|instructions?|guidelines?|"
    r"persona|behavior|behaviour|assistant|model|claude|gpt|gemini|grok|"
    r"rules|policy|safety|refus|knowledge cutoff|tone|formatting|"
    r"tone|memory|tools?|examples?|anthropic|openai|google|xai)",
    re.IGNORECASE
)


def is_likely_prompt(entry):
    """Heurística: é provavelmente um system prompt?"""
    p = entry["path"]
    if any(pat.search(p) for pat in NOT_PROMPT_PATTERNS):
        return False
    # Tamanho mínimo razoável pra um prompt real
    if entry["tokens_estimate"] < 50:
        return False
    # Precisa de keywords OU ser de pasta conhecida
    if PROMPT_KEYWORDS.search(entry["filename"]):
        return True
    if PROMPT_KEYWORDS.search(entry.get("persona", "")):
        return True
    if entry.get("xml_tags") and len(entry["xml_tags"]) >= 2:
        return True
    # Path heuristic
    path_lower = p.lower()
    if any(kw in path_lower for kw in ["prompt", "system", "agent", "cowork", "design", "code"]):
        return True
    return False


def main():
    raw = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    print(f"Total raw: {len(raw)}")
    filtered = [p for p in raw if is_likely_prompt(p)]
    print(f"Filtered: {len(filtered)}")
    # Salva
    out = Path("/workspace/meta-prompt-engine/data/index_filtered.json")
    out.write_text(json.dumps(filtered, indent=2, ensure_ascii=False))
    print(f"Salvo em {out}")
    # Stats por empresa
    from collections import Counter
    by_co = Counter(p["company"] for p in filtered)
    print("\nPor empresa (filtrado):")
    for c, n in by_co.most_common():
        print(f"  {c}: {n}")


if __name__ == "__main__":
    main()
