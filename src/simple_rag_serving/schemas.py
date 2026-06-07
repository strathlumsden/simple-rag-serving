from pydantic import BaseModel, Field, field_validator


class QueryRequest(BaseModel):
    query: str
    top_k: int = Field(default=3, ge=1)

    @field_validator("query")
    @classmethod
    def query_must_not_be_blank(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            msg = "query must not be empty"
            raise ValueError(msg)
        return stripped


class RetrievedSource(BaseModel):
    document_id: str
    text: str
    score: float | None = None
    metadata: dict[str, str] = Field(default_factory=dict)


class QueryResponse(BaseModel):
    answer: str
    sources: list[RetrievedSource]
