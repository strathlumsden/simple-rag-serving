# AGENTS.md

## Project overview

This is a lightweight FastAPI-based RAG serving project.

The goal is to demonstrate a modular RAG pipeline:

query → embedding → retrieval → prompt construction → generation → response

Prefer simple, explicit components over framework-heavy abstractions.

## Development commands

Use `uv` for dependency and environment management.

Install dependencies:

```bash
uv sync --dev
```

Run tests:

```bash
uv run pytest
```

Run linting:

```bash
uv run ruff check .
```

Run formatting check:

```bash
uv run ruff format --check .
```

Run the local API server:

```bash
uv run uvicorn simple_rag_serving.main:app --reload
```

Before finishing a code task, run:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

## Project structure

* `src/simple_rag_serving/main.py`: FastAPI app entrypoint only.
* `src/simple_rag_serving/api.py`: FastAPI app creation, routes, and lifespan setup.
* `src/simple_rag_serving/schemas.py`: Pydantic request/response schemas.
* `src/simple_rag_serving/config.py`: Pydantic configuration objects.
* `src/simple_rag_serving/embeddings.py`: embedding model wrapper.
* `src/simple_rag_serving/vector_store.py`: vector store interface and local in-memory implementation.
* `src/simple_rag_serving/retrieval.py`: query-time retrieval logic.
* `src/simple_rag_serving/prompts.py`: prompt construction.
* `src/simple_rag_serving/generation.py`: LLM/text-generation wrapper.
* `src/simple_rag_serving/rag.py`: orchestration of retrieval + generation.
* `tests/`: pytest tests.

## Architecture rules

* Keep `main.py` minimal.
* Keep FastAPI route handlers thin.
* Do not put retrieval, embedding, prompt, or generation logic directly in route handlers.
* Keep request/response contracts in `schemas.py`.
* Keep model/provider-specific code behind small wrapper classes or functions.
* Keep vector database details behind the vector store abstraction.
* Do not add queueing, batching, streaming, Docker, or cloud code unless explicitly requested.
* Do not add LangChain, LlamaIndex, or a real vector database unless explicitly requested.

## RAG design rules

* The online path should be: query → embed query → retrieve chunks → build prompt → generate answer → return response.
* Return retrieved sources where possible.
* Keep prompt construction isolated in `prompts.py`.
* Keep generation isolated in `generation.py`.
* Keep retrieval isolated in `retrieval.py`.
* Prefer small interfaces that allow swapping implementations later.

## Testing expectations

Add or update tests for every behavior change.

Tests should use small synthetic documents.

Tests should cover:

* schema validation
* in-memory vector search
* retrieval top-k behavior
* prompt construction
* RAG orchestration
* FastAPI route smoke tests

Do not require GPU, external APIs, real vector databases, or downloaded large models in unit tests unless explicitly requested.

## Data, secrets, and artifacts

Do not commit:

* `.env`
* API keys
* downloaded model weights
* generated embeddings
* vector indexes
* caches
* large documents
* private data

Small synthetic example documents may live in:

```text
data/examples/
```

Generated local outputs should live in:

```text
artifacts/
```

and should be ignored by Git.

## Dependency rules

Do not add new dependencies unless needed for the current task.

Ask before adding heavy dependencies such as:

* torch
* transformers
* langchain
* llama-index
* qdrant-client
* pinecone
* faiss
* vllm

Preferred baseline dependencies:

* fastapi
* uvicorn
* pydantic
* numpy
* pytest
* ruff

## Coding style

* Use Python 3.11+ syntax.
* Use type hints.
* Prefer small, testable functions.
* Prefer `pathlib.Path` for paths.
* Avoid hidden global state where practical.
* Avoid hardcoded absolute paths.
* Keep error messages clear.

## Agent workflow

For non-trivial tasks:

1. Inspect relevant files.
2. Propose a short plan before editing.
3. Keep the diff focused.
4. Modify only files needed for the task.
5. Add or update tests.
6. Run linting and tests.
7. Summarize changed files, assumptions, and test results.

## Definition of done

A task is done when:

* implementation matches the requested scope
* relevant tests are added or updated
* `uv run ruff check .` passes
* `uv run ruff format --check .` passes
* `uv run pytest` passes
* no unrelated files are changed
* no generated artifacts or secrets are committed

## Do not do

* Do not redesign the whole project.
* Do not add production infrastructure unless requested.
* Do not silently change public schemas.
* Do not introduce external services into tests.
* Do not commit generated artifacts.
