import pytest
from pydantic import ValidationError

from simple_rag_serving.schemas import QueryRequest, QueryResponse, RetrievedSource


def test_query_request_accepts_valid_query() -> None:
    request = QueryRequest(query="What is RAG?", top_k=5)

    assert request.query == "What is RAG?"
    assert request.top_k == 5


def test_query_request_uses_default_top_k() -> None:
    request = QueryRequest(query="What is RAG?")

    assert request.top_k == 3


@pytest.mark.parametrize("query", ["", "   ", "\n\t"])
def test_query_request_rejects_blank_query(query: str) -> None:
    with pytest.raises(ValidationError):
        QueryRequest(query=query)


@pytest.mark.parametrize("top_k", [0, -1])
def test_query_request_rejects_invalid_top_k(top_k: int) -> None:
    with pytest.raises(ValidationError):
        QueryRequest(query="What is RAG?", top_k=top_k)


def test_query_response_serializes_source_with_optional_fields() -> None:
    response = QueryResponse(
        answer="RAG combines retrieval and generation.",
        sources=[
            RetrievedSource(
                document_id="doc-1",
                text="RAG retrieves relevant context before generation.",
                score=0.92,
                metadata={"title": "RAG overview"},
            )
        ],
    )

    assert response.model_dump() == {
        "answer": "RAG combines retrieval and generation.",
        "sources": [
            {
                "document_id": "doc-1",
                "text": "RAG retrieves relevant context before generation.",
                "score": 0.92,
                "metadata": {"title": "RAG overview"},
            }
        ],
    }


def test_retrieved_source_uses_safe_defaults() -> None:
    source = RetrievedSource(document_id="doc-1", text="A short source chunk.")

    assert source.score is None
    assert source.metadata == {}
