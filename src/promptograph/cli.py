"""promptograph.cli — Ponto de entrada CLI e MCP para o Promptograph.

Uso:
    promptograph               # Inicia o servidor FastMCP stdio (padrão para uvx e Claude Desktop/Cursor)
    promptograph mcp           # Inicia o servidor FastMCP stdio
    promptograph web [8765]    # Inicia a interface web offline zero-dependency
    promptograph search <term> # Busca rápida em 20.475 prompts
    promptograph stats         # Exibe métricas globais do acervo
    promptograph validate <txt># Valida qualidade de um system prompt
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _run_mcp():
    from promptograph.mcp_server import main as mcp_main
    mcp_main()


def _run_web(port: int = 8765):
    import http.server
    import socketserver
    import webbrowser
    from promptograph.skills_registry import search_skills, get_skill_blueprint, get_skills_stats
    import json

    pkg_dir = Path(__file__).resolve().parent
    static_dir = pkg_dir / "static"
    if not static_dir.exists():
        repo_static = pkg_dir.parent.parent / "static"
        if repo_static.exists():
            static_dir = repo_static

    print(f"🚀 Iniciando Promptograph Web UI em http://localhost:{port}")
    print(f"   Arquivos estáticos: {static_dir}")
    print("   Pressione Ctrl+C para encerrar.")

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(static_dir), **kwargs)

        def do_GET(self):
            if self.path.startswith("/api/skills/categories"):
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(get_skills_stats(), ensure_ascii=False).encode("utf-8"))
                return
            if self.path.startswith("/api/skills"):
                from urllib.parse import urlparse, parse_qs
                parsed = urlparse(self.path)
                params = parse_qs(parsed.query)
                q = params.get("q", [""])[0]
                cat = params.get("category", [""])[0]
                limit = int(params.get("limit", [50])[0])
                res = search_skills(query=q, category=cat, limit=limit)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
                return
            return super().do_GET()

    with socketserver.TCPServer(("", port), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nEncerrando servidor web.")


def _run_search(query: str, limit: int = 15):
    from promptograph.mcp_server import _INDEX
    q_lower = query.lower().strip()
    hits = []
    for p in _INDEX:
        text = f"{p.get('filename','')} {p.get('persona','')} {p.get('company','')} {p.get('model','')}".lower()
        if q_lower in text:
            hits.append(p)
            if len(hits) >= limit:
                break
    print(f"\nBusca por '{query}' — {len(hits)} resultado(s):")
    print("=" * 65)
    for i, h in enumerate(hits, 1):
        print(f"[{i}] {h.get('filename')} | {h.get('company')} | {h.get('model')}")
        print(f"    Persona: {h.get('persona') or 'Geral'}")
        print(f"    Tokens: ~{h.get('tokens'):,} | {h.get('preview')[:120]}...\n")


def _run_stats():
    from promptograph.mcp_server import promptograph_stats
    print(promptograph_stats())


def _run_validate(content: str):
    from promptograph import validate_prompt
    res = validate_prompt(content)
    print("=" * 65)
    print(f"Nota: {res['grade']} ({res['score']}%)")
    print(f"Diagnóstico: {res['summary']}")
    print("=" * 65)


def main():
    if len(sys.argv) == 1:
        # Padrão: inicia MCP stdio para uvx / clientes MCP
        _run_mcp()
        return

    arg = sys.argv[1].lower()

    if arg in ("mcp", "--mcp", "-m"):
        _run_mcp()
    elif arg in ("web", "--web", "-w"):
        port = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 8765
        _run_web(port)
    elif arg in ("stats", "--stats", "-s"):
        _run_stats()
    elif arg in ("validate", "--validate", "-v"):
        txt = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        if not txt:
            print("Uso: promptograph validate <texto do prompt>")
            sys.exit(1)
        _run_validate(txt)
    elif arg in ("search", "--search"):
        q = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        _run_search(q)
    elif arg in ("-h", "--help", "help"):
        print(__doc__)
    else:
        # Se passou uma query solta, executa search
        _run_search(" ".join(sys.argv[1:]))


if __name__ == "__main__":
    main()
