from pydantic import BaseModel, Field

from simple_rag_serving.documents import Document


class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str
    chunk_index: int
    text: str
    metadata: dict[str, str] = Field(default_factory=dict)


def chunk_document(
    document: Document,
    chunk_size: int,
    overlap: int = 0,
) -> list[DocumentChunk]:
    _validate_chunking_args(chunk_size, overlap)

    words = document.text.split()
    step = chunk_size - overlap
    chunks: list[DocumentChunk] = []

    for chunk_index, start in enumerate(range(0, len(words), step)):
        chunk_words = words[start : start + chunk_size]
        if not chunk_words:
            continue

        chunks.append(
            DocumentChunk(
                chunk_id=f"{document.document_id}::chunk-{chunk_index}",
                document_id=document.document_id,
                chunk_index=chunk_index,
                text=" ".join(chunk_words),
                metadata=document.metadata.copy(),
            )
        )

        if start + chunk_size >= len(words):
            break

    return chunks


def chunk_documents(
    documents: list[Document],
    chunk_size: int,
    overlap: int = 0,
) -> list[DocumentChunk]:
    chunks: list[DocumentChunk] = []

    for document in documents:
        chunks.extend(
            chunk_document(document=document, chunk_size=chunk_size, overlap=overlap)
        )

    return chunks


def _validate_chunking_args(chunk_size: int, overlap: int) -> None:
    if chunk_size <= 0:
        msg = "chunk_size must be greater than 0"
        raise ValueError(msg)
    if overlap < 0:
        msg = "overlap must be greater than or equal to 0"
        raise ValueError(msg)
    if overlap >= chunk_size:
        msg = "overlap must be less than chunk_size"
        raise ValueError(msg)
