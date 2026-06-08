import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, ValidationError, field_validator


class Document(BaseModel):
    document_id: str
    text: str
    metadata: dict[str, str] = Field(default_factory=dict)

    @field_validator("document_id", "text")
    @classmethod
    def text_field_must_not_be_blank(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            msg = "field must not be empty"
            raise ValueError(msg)
        return stripped


def load_documents(path: Path) -> list[Document]:
    documents: list[Document] = []

    with path.open(encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            documents.append(_parse_document_line(line, line_number))

    return documents


def _parse_document_line(line: str, line_number: int) -> Document:
    try:
        record: Any = json.loads(line)
    except json.JSONDecodeError as exc:
        msg = f"Invalid JSON on line {line_number}: {exc.msg}"
        raise ValueError(msg) from exc

    try:
        return Document.model_validate(record)
    except ValidationError as exc:
        msg = f"Invalid document on line {line_number}: {exc}"
        raise ValueError(msg) from exc
