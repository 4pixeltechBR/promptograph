#!/usr/bin/env python3
"""server.py — Servidor HTTP standalone para o Promptograph (Python 3.10+ stdlib only).

Zero dependências externas. Serve:
  - Frontend estático (HTML/JS/CSS)
  - API REST de System Prompts (20.475 prompts indexados)
  - API REST do Arsenal de Skills Curadas (226+ skills em 37 categorias)
  - API de Diff, Validação Heurística e Geração de Prompts
"""

from __future__ import annotations

import difflib
import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# Path setup
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

STATIC = ROOT / "static"
INDEX_PATH = ROOT / "data" / "index_filtered.json"
SKILLS_MANIFEST_PATH = ROOT / "data" / "skills_manifest.json"
ARCHIVE = Path(os.getenv("PROMPTOGRAPH_ARCHIVE_PATH", "/workspace/leaked-prompts-archive"))

# Imports de módulos internos
try:
    from validators.quality import validate_prompt
except Exception:
    from src.skills.promptograph.validator import validate_prompt

try:
    from generator.builder import PRESET_TEMPLATES, build_prompt
except Exception:
    from src.skills.promptograph.builder import PRESET_TEMPLATES, build_prompt


# ── Carrega índice unificado de 20.475 prompts ─────────────────────────

def _load_prompts() -> list[dict]:
    if not INDEX_PATH.exists():
        print(f"[Init] Aviso: {INDEX_PATH} não encontrado")
        return []

    try:
        raw = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        entries = raw.get("entries", []) if isinstance(raw, dict) else raw
        prompts = []
        for p in entries:
            path = p.get("path", "")
            pid = p.get("id") or path.replace("/", "__").replace("\\", "__")
            prompts.append({
                "id": pid,
                "path": path,
                "filename": p.get("filename") or Path(path).name,
                "company": p.get("company", "Community/OpenSource"),
                "model": p.get("model") or p.get("title", ""),
                "size_bytes": p.get("size_bytes", 0),
                "words": p.get("words", 0),
                "tokens_estimate": p.get("tokens_estimate") or (p.get("words", 0) * 4 // 3) or (p.get("size_bytes", 0) // 4),
                "persona": p.get("persona", ""),
                "preview": p.get("preview", ""),
            })
        print(f"[Init] Loaded {len(prompts)} prompts from index")
        return prompts
    except Exception as e:
        print(f"[Init] Erro ao carregar prompts: {e}")
        return []


INDEX = _load_prompts()

# ── Carrega manifesto de skills ────────────────────────────────────────

def _load_skills() -> list[dict]:
    if not SKILLS_MANIFEST_PATH.exists():
        return []
    try:
        return json.loads(SKILLS_MANIFEST_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[Init] Erro ao carregar skills: {e}")
        return []


SKILLS = _load_skills()
print(f"[Init] Loaded {len(SKILLS)} curated skills from manifest")


# ── Cache do conteúdo raw ──────────────────────────────────────────────

RAW_CACHE: dict[str, str] = {}


def get_raw(prompt_id: str) -> str:
    """Recupera o conteúdo raw do arquivo a partir do id."""
    if prompt_id in RAW_CACHE:
        return RAW_CACHE[prompt_id]
    p = next((x for x in INDEX if x["id"] == prompt_id), None)
    if not p:
        return ""
    full = ARCHIVE / p["path"]
    if not full.exists():
        # Fallback local se o arquivo estiver dentro do repo
        local_full = ROOT / "data" / p["path"]
        if local_full.exists():
            full = local_full
        else:
            return p.get("preview", "")

    try:
        content = full.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        content = ""
    RAW_CACHE[prompt_id] = content
    return content


def make_diff_html(left_text: str, right_text: str) -> str:
    """Gera HTML de diff usando difflib."""
    left_lines = left_text.splitlines(keepends=True)
    right_lines = right_text.splitlines(keepends=True)
    diff = difflib.unified_diff(left_lines, right_lines, lineterm="", n=2)
    html_lines = []
    for line in diff:
        line_esc = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("@@"):
            html_lines.append(f'<span class="ctx">{line_esc.rstrip()}</span>')
        elif line.startswith("+"):
            html_lines.append(f'<span class="add">{line_esc.rstrip()}</span>')
        elif line.startswith("-"):
            html_lines.append(f'<span class="rem">{line_esc.rstrip()}</span>')
        else:
            html_lines.append(f'<span class="ctx">{line_esc.rstrip()}</span>')
    return "\n".join(html_lines[:5000])


# ── Request Handler ────────────────────────────────────────────────────

class Handler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Silencia logs comuns

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: Path, content_type="text/plain"):
        if not path.exists():
            self.send_response(404)
            self.end_headers()
            return
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        path = url.path

        # UI e estáticos
        if path == "/":
            return self._send_file(STATIC / "index.html", "text/html; charset=utf-8")
        if path.startswith("/static/"):
            return self._send_file(STATIC / path[len("/static/"):])

        # API de Prompts
        if path == "/api/index":
            return self._send_json(INDEX)

        if path == "/api/raw":
            qs = parse_qs(url.query)
            pid = qs.get("id", [None])[0]
            if not pid:
                return self._send_json({"error": "missing id"}, 400)
            content = get_raw(pid)
            return self._send_json({"content": content, "len": len(content)})

        if path.startswith("/api/presets/"):
            name = path[len("/api/presets/"):]
            if name in PRESET_TEMPLATES:
                return self._send_json(PRESET_TEMPLATES[name])
            return self._send_json({"error": "not found"}, 404)

        if path == "/api/stats":
            from collections import defaultdict
            by_co = defaultdict(int)
            for p in INDEX:
                by_co[p.get("company", "Other")] += 1
            return self._send_json({
                "total": len(INDEX),
                "by_company": dict(by_co),
                "total_tokens": sum(p.get("tokens_estimate", 0) for p in INDEX),
                "skills_count": len(SKILLS),
            })

        # API de Skills Curadas (v0.3.1)
        if path == "/api/skills":
            qs = parse_qs(url.query)
            q = (qs.get("q", [""])[0]).lower().strip()
            cat = (qs.get("category", [""])[0]).lower().strip()

            filtered = SKILLS
            if cat:
                filtered = [s for s in filtered if cat in s.get("category", "").lower()]
            if q:
                filtered = [s for s in filtered if q in s.get("name", "").lower() or q in s.get("description", "").lower() or q in " ".join(s.get("tags", [])).lower()]

            return self._send_json({"total": len(filtered), "skills": filtered})

        if path == "/api/skills/blueprint":
            qs = parse_qs(url.query)
            sid = qs.get("id", [""])[0].lower().strip()
            match = next((s for s in SKILLS if s.get("id", "").lower() == sid or s.get("name", "").lower() == sid), None)
            if match:
                return self._send_json(match)
            return self._send_json({"error": "Skill não encontrada"}, 404)

        if path == "/api/skills/categories":
            from collections import Counter
            cat_counts = Counter(s.get("category", "Outros") for s in SKILLS)
            return self._send_json({"total_categories": len(cat_counts), "categories": dict(cat_counts.most_common())})

        # Default: 404
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        url = urlparse(self.path)
        path = url.path
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length else "{}"
        try:
            data = json.loads(body)
        except Exception:
            data = {}

        if path == "/api/diff":
            left = get_raw(data.get("left", ""))
            right = get_raw(data.get("right", ""))
            left_size = len(left) // 4
            right_size = len(right) // 4
            diff_html = make_diff_html(left, right)
            return self._send_json({
                "left_tokens": left_size,
                "right_tokens": right_size,
                "diff_html": diff_html,
            })

        if path == "/api/validate":
            content = data.get("content", "")
            result = validate_prompt(content)
            return self._send_json(result)

        if path == "/api/generate":
            spec = data.get("spec", {})
            prompt = build_prompt(spec)
            val = validate_prompt(prompt)
            return self._send_json({
                "prompt": prompt,
                "score": val["score"],
                "grade": val["grade"],
                "passed": val["passed"],
                "failed": val["failed"],
                "chars": len(prompt),
                "tokens": len(prompt) // 4,
            })

        self.send_response(404)
        self.end_headers()


def run(port=8765):
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"🚀 Promptograph server v0.3.1 running on http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    run(port)
