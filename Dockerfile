FROM python:3.12-slim

LABEL org.opencontainers.image.title="Meta-Prompt Engine"
LABEL org.opencontainers.image.description="Browse, diff, validate and generate AI system prompts"
LABEL org.opencontainers.image.source="https://github.com/YOUR_USER/meta-prompt-engine"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app

# Copy only what we need (small image)
COPY server.py ./
COPY generator/ ./generator/
COPY validators/ ./validators/
COPY static/ ./static/
COPY data/index_filtered.json ./data/index_filtered.json

# Expose port
EXPOSE 8765

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8765/api/stats')" || exit 1

# Run
CMD ["python3", "server.py", "8765"]
