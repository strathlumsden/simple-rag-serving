# Simple RAG Serving

A lightweight FastAPI service that demonstrates the core RAG serving path: query embedding, vector retrieval, prompt construction, and answer generation.

## Status

Local prototype.

## Goal

Build a modular RAG service where each component can later be replaced with a more production-ready implementation.

## Non-goals

- No production vector database yet.
- No streaming responses yet.
- No authentication yet.
- No external document ingestion pipeline yet.
- No production-grade batching or load balancing yet.

## Planned architecture

query → embed → retrieve → build prompt → generate → respond

## Development

```bash
uv sync --dev
uv run pytest
uv run ruff check .
uv run uvicorn simple_rag_serving.main:app --reload
```


