"""
server.py — Backend do Meta-Prompt Engine.
Servidor HTTP em Python puro (stdlib), serve a UI e a API.
"""

import json
import os
import sys
import re
import difflib
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

# Adiciona path
sys.path.insert(0, str(Path(__file__).parent))
from generator.builder import build_prompt, PRESET_TEMPLATES
from validators.quality import validate_prompt as do_validate

ROOT = Path(__file__).parent
ARCHIVE = Path("/workspace/leaked-prompts-archive")
STATIC = ROOT / "static"
INDEX_PATH = ROOT / "data" / "index_filtered.json"  # Usa o filtrado (sem READMEs)

# Carrega índice em memória
INDEX = []
if INDEX_PATH.exists():
    INDEX = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    print(f"[Init] Loaded {len(INDEX)} prompts from filtered index")

# Cache do conteúdo raw
RAW_CACHE = {}


def get_raw(prompt_id: str) -> str:
    """Recupera o conteúdo raw do arquivo a partir do id."""
    if prompt_id in RAW_CACHE:
        return RAW_CACHE[prompt_id]
    p = next((x for x in INDEX if x["id"] == prompt_id), None)
    if not p:
        return ""
    full = ARCHIVE / p["path"]
    if not full.exists():
        return ""
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
    return "\n".join(html_lines[:5000])  # Limita a 5000 linhas


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Silencia log

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
        # API
        if path == "/api/index":
            return self._send_json(INDEX)
        if path == "/":
            return self._send_file(STATIC / "index.html", "text/html; charset=utf-8")
        if path.startswith("/static/"):
            return self._send_file(STATIC / path[len("/static/"):])
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
                by_co[p["company"]] += 1
            return self._send_json({
                "total": len(INDEX),
                "by_company": dict(by_co),
                "total_tokens": sum(p["tokens_estimate"] for p in INDEX),
            })
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
            diff = right_size - left_size
            diff_pct = round((diff / max(left_size, 1)) * 100, 1)
            diff_html = make_diff_html(left, right)
            # Conta added/removed
            added = sum(1 for l in diff_html.split("\n") if '<span class="add">' in l)
            removed = sum(1 for l in diff_html.split("\n") if '<span class="rem">' in l)
            return self._send_json({
                "left_size": left_size,
                "right_size": right_size,
                "diff_tokens": diff,
                "diff_pct": diff_pct,
                "added": added,
                "removed": removed,
                "diff_html": diff_html,
            })

        if path == "/api/validate":
            content = data.get("content", "")
            result = do_validate(content)
            return self._send_json(result)

        if path == "/api/generate":
            spec = data
            prompt = build_prompt(spec)
            return self._send_json({
                "prompt": prompt,
                "chars": len(prompt),
                "tokens": len(prompt) // 4,
            })

        self.send_response(404)
        self.end_headers()


def main(port=8765):
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"[Server] Promptograph rodando em http://localhost:{port}")
    print(f"[Server] Index tem {len(INDEX)} prompts")
    print(f"[Server] Pressione Ctrl+C pra parar")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[Server] Parando...")


if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    main(port)
