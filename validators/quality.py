"""
validators/quality.py — Valida qualidade de um system prompt baseado em boas práticas
extraídas dos repos analisados (Claude Fable 5, GPT-5, Gemini, Cursor, Devin, etc).
"""

import re


# Padrões identificados a partir dos repos analisados
GOOD_PRACTICES = {
    "identity_clarity": {
        "weight": 15,
        "description": "Define claramente a identidade/persona (ex: 'You are X, built by Y')",
        "check": lambda c: bool(re.search(r"You are\s+\w", c) or re.search(r"Você é\s+\w", c) or re.search(r"I am\s+\w", c) or re.search(r"identif", c, re.IGNORECASE)),
    },
    "knowledge_cutoff": {
        "weight": 5,
        "description": "Menciona knowledge cutoff ou data atual",
        "check": lambda c: bool(re.search(r"(knowledge cutoff|cutoff|knowledge_cutoff|data atual|current date)", c, re.IGNORECASE)),
    },
    "tone_guidelines": {
        "weight": 10,
        "description": "Define tom de voz (warm, professional, concise, etc)",
        "check": lambda c: bool(re.search(r"\b(warm|professional|concise|friendly|empathetic|kind|polite|neutral|objective)\b", c, re.IGNORECASE)),
    },
    "formatting_rules": {
        "weight": 8,
        "description": "Especifica regras de formatação (bullets, headers, listas, markdown)",
        "check": lambda c: bool(re.search(r"\b(bullet|list|markdown|header|heading|format|prose|paragraph)\b", c, re.IGNORECASE)),
    },
    "refusals_handling": {
        "weight": 10,
        "description": "Define quando/como recusar pedidos",
        "check": lambda c: bool(re.search(r"\b(refuse|decline|reject|cannot|can'?t|won'?t|not (provide|generate|create))\b", c, re.IGNORECASE)),
    },
    "safety_rules": {
        "weight": 10,
        "description": "Inclui regras de segurança (child safety, weapons, drugs, etc)",
        "check": lambda c: bool(re.search(r"\b(safet|harm|child|minor|weapon|drug|illegal|illicit|exploit|malware|violent)\b", c, re.IGNORECASE)),
    },
    "tool_usage": {
        "weight": 8,
        "description": "Documenta tools disponíveis e quando usar",
        "check": lambda c: bool(re.search(r"\b(tool|function call|tool_use|json|mcp|plugin)\b", c, re.IGNORECASE)),
    },
    "examples_section": {
        "weight": 10,
        "description": "Inclui exemplos few-shot (good vs bad responses)",
        "check": lambda c: bool(re.search(r"\b(example|few-shot|demonstration)\b", c, re.IGNORECASE)),
    },
    "memory_or_context": {
        "weight": 6,
        "description": "Define como gerenciar contexto/memória entre turns",
        "check": lambda c: bool(re.search(r"\b(memory|context|conversation history|previous)\b", c, re.IGNORECASE)),
    },
    "structured_tags": {
        "weight": 5,
        "description": "Usa tags XML/estruturadas para organizar seções",
        "check": lambda c: bool(re.search(r"<\w+>", c)),
    },
    "citation_or_sources": {
        "weight": 5,
        "description": "Menciona regras de citação/fontes",
        "check": lambda c: bool(re.search(r"\b(cite|citation|source|reference|attribut)\b", c, re.IGNORECASE)),
    },
    "limits_and_boundaries": {
        "weight": 5,
        "description": "Define limites claros (o que NÃO fazer)",
        "check": lambda c: bool(re.search(r"\b(never|do not|don'?t|avoid|shouldn'?t|must not|prohibit)\b", c, re.IGNORECASE)),
    },
    "length_appropriateness": {
        "weight": 3,
        "description": "Tamanho razoável (nem muito curto nem excessivo)",
        "check": lambda c: 200 <= len(c) <= 200_000,
    },
}

# Red flags / problemas comuns
RED_FLAGS = {
    "vague_identity": {
        "description": "Identidade vaga ou ausente",
        "check": lambda c: not re.search(r"You are\s+\w", c) and not re.search(r"Você é\s+\w", c),
    },
    "instruction_contradiction": {
        "description": "Possíveis contradições ('always' + 'never' no mesmo contexto)",
        "check": lambda c: len(re.findall(r"\b(always|never)\b", c, re.IGNORECASE)) > 20,
    },
    "jailbreak_vulnerability": {
        "description": "Não menciona proteção contra prompt injection",
        "check": lambda c: not re.search(r"\b(prompt injection|jailbreak|adversarial|ignore previous|ignore the above)\b", c, re.IGNORECASE),
    },
    "copyright_missing": {
        "description": "Não menciona regras de copyright",
        "check": lambda c: not re.search(r"\b(copyright|fair use|reproduce|trademark)\b", c, re.IGNORECASE),
    },
    "too_short": {
        "description": "Muito curto para ser um system prompt útil",
        "check": lambda c: len(c) < 200,
    },
    "too_long_warning": {
        "description": "Pode ser excessivamente longo (>100k tokens) - considere trim",
        "check": lambda c: len(c) > 400_000,
    },
}


def validate_prompt(content: str) -> dict:
    """Valida um system prompt e retorna score + detalhes."""
    if not content or len(content.strip()) < 50:
        return {
            "score": 0,
            "grade": "F",
            "passed": [],
            "failed": ["too_short"],
            "warnings": ["Prompt vazio ou inválido"],
            "summary": "Conteúdo insuficiente para análise."
        }

    passed = []
    failed = []
    total_score = 0
    total_weight = sum(p["weight"] for p in GOOD_PRACTICES.values())

    for key, practice in GOOD_PRACTICES.items():
        if practice["check"](content):
            passed.append({"key": key, "description": practice["description"]})
            total_score += practice["weight"]
        else:
            failed.append({"key": key, "description": practice["description"]})

    warnings = []
    for key, flag in RED_FLAGS.items():
        if flag["check"](content):
            warnings.append({"key": key, "description": flag["description"]})

    score_pct = round((total_score / total_weight) * 100, 1)
    if score_pct >= 90: grade = "A+"
    elif score_pct >= 80: grade = "A"
    elif score_pct >= 70: grade = "B"
    elif score_pct >= 60: grade = "C"
    elif score_pct >= 50: grade = "D"
    else: grade = "F"

    # Summary humanizado
    if score_pct >= 80:
        verdict = "Excelente — segue as melhores práticas observadas nos principais modelos."
    elif score_pct >= 60:
        verdict = "Bom — alguns pontos podem ser melhorados."
    elif score_pct >= 40:
        verdict = "Razoável — vale revisar as seções faltantes."
    else:
        verdict = "Fraco — considere reescrever seguindo os padrões dos modelos de referência."

    return {
        "score": score_pct,
        "grade": grade,
        "passed": passed,
        "failed": failed,
        "warnings": warnings,
        "summary": verdict,
        "stats": {
            "chars": len(content),
            "words": len(content.split()),
            "lines": content.count("\n") + 1,
            "tokens_estimate": len(content) // 4,
        }
    }


if __name__ == "__main__":
    import sys
    test = """You are Claude, an AI assistant built by Anthropic.
    You should be warm, helpful, and concise. Never lie. Always provide citations.
    Safety: avoid generating harmful content. Refuse requests for weapons.
    Use markdown formatting. Do not reproduce copyrighted material."""
    result = validate_prompt(test)
    print(f"Score: {result['score']} ({result['grade']})")
    print(f"Verdict: {result['summary']}")
    print(f"Passed: {len(result['passed'])}/{len(result['passed']) + len(result['failed'])}")
    print(f"Warnings: {len(result['warnings'])}")
