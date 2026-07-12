#!/usr/bin/env bash
# bootstrap.sh — One-command setup for Promptograph
# Builds the prompt index from source repos (if available) or uses the
# pre-built index shipped in data/index_filtered.json.

set -e

echo "📷 Promptograph — bootstrap"
echo "   Photograph every system prompt that matters."
echo ""

# Check Python
if ! command -v python3 >/dev/null 2>&1; then
    echo "❌ Python 3 is required but not installed"
    echo "   Install from https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Python $PYTHON_VERSION found"

# Check if archive exists
if [ -d "/workspace/leaked-prompts-archive" ] || [ -d "../leaked-prompts-archive" ]; then
    echo ""
    echo "📦 Source archive detected. Building fresh index..."
    if [ -d "/workspace/leaked-prompts-archive" ]; then
        ARCHIVE_PATH="/workspace/leaked-prompts-archive"
    else
        ARCHIVE_PATH="../leaked-prompts-archive"
    fi
    echo "   Scanning $ARCHIVE_PATH ..."
    python3 -c "
import sys
sys.path.insert(0, '.')
import os
import generator.parser as p
p.ARCHIVE_PATH = __import__('pathlib').Path('$ARCHIVE_PATH')
prompts = p.scan_all_repos()
print(f'   Found {len(prompts)} prompts')
"
    python3 generator/refine_index.py
else
    echo ""
    echo "ℹ️  No source archive found at /workspace/leaked-prompts-archive"
    echo "   Using pre-built index in data/index_filtered.json"
fi

# Verify index
if [ ! -f "data/index_filtered.json" ]; then
    echo "❌ No index found. Build failed?"
    exit 1
fi

INDEX_SIZE=$(stat -c%s "data/index_filtered.json" 2>/dev/null || stat -f%z "data/index_filtered.json" 2>/dev/null)
PROMPT_COUNT=$(python3 -c "import json; print(len(json.load(open('data/index_filtered.json'))))")
echo ""
echo "✅ Index ready: $PROMPT_COUNT prompts ($((INDEX_SIZE/1024)) KB)"

# Smoke test
echo ""
echo "🧪 Running smoke test..."
python3 -c "
import sys
sys.path.insert(0, '.')
from generator.builder import build_prompt, PRESET_TEMPLATES
from validators.quality import validate_prompt
spec = PRESET_TEMPLATES['claude_coding_agent']['spec']
prompt = build_prompt(spec)
result = validate_prompt(prompt)
print(f'   Generated: {len(prompt)} chars, ~{len(prompt)//4} tokens')
print(f'   Validation: {result[\"score\"]}% ({result[\"grade\"]})')
"

echo ""
echo "🎉 Bootstrap complete!"
echo ""
echo "To start the server:"
echo "  python3 server.py 8765"
echo ""
echo "Then open: http://localhost:8765"
