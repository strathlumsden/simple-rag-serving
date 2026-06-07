from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class RagConfig(BaseModel):
    embedding_model_name: str = "intfloat/multilingual-e5-large-instruct"
    generation_model_name: str = "facebook/opt-125m"
    documents_path: Path = Field(default=Path("data/examples/documents.jsonl"))

    @field_validator("embedding_model_name", "generation_model_name")
    @classmethod
    def model_name_must_not_be_blank(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            msg = "model name must not be empty"
            raise ValueError(msg)
        return stripped

    @field_validator("documents_path", mode="before")
    @classmethod
    def documents_path_must_not_be_blank(cls, value: object) -> object:
        if isinstance(value, str) and not value.strip():
            msg = "documents_path must not be empty"
            raise ValueError(msg)
        return value
