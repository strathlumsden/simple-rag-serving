import pytest

from simple_rag_serving.chunking import chunk_document, chunk_documents
from simple_rag_serving.documents import Document


def test_chunk_document_creates_one_chunk_for_short_document() -> None:
    document = Document(document_id="doc-1", text="one two three")

    chunks = chunk_document(document=document, chunk_size=5)

    assert len(chunks) == 1
    assert chunks[0].text == "one two three"


def test_chunk_document_creates_multiple_chunks_for_long_document() -> None:
    document = Document(document_id="doc-1", text="one two three four five six")

    chunks = chunk_document(document=document, chunk_size=3)

    assert [chunk.text for chunk in chunks] == [
        "one two three",
        "four five six",
    ]


def test_chunk_document_preserves_identity_and_metadata() -> None:
    document = Document(
        document_id="doc-1",
        text="one two three four",
        metadata={"topic": "numbers"},
    )

    chunks = chunk_document(document=document, chunk_size=2)

    assert chunks[0].chunk_id == "doc-1::chunk-0"
    assert chunks[0].document_id == "doc-1"
    assert chunks[0].chunk_index == 0
    assert chunks[0].metadata == {"topic": "numbers"}
    assert chunks[1].chunk_id == "doc-1::chunk-1"
    assert chunks[1].chunk_index == 1


def test_chunk_document_copies_metadata_per_chunk() -> None:
    document = Document(
        document_id="doc-1",
        text="one two three four",
        metadata={"topic": "numbers"},
    )

    chunks = chunk_document(document=document, chunk_size=2)
    chunks[0].metadata["topic"] = "changed"

    assert chunks[1].metadata == {"topic": "numbers"}


def test_chunk_document_uses_overlap_windows() -> None:
    document = Document(document_id="doc-1", text="one two three four five six seven")

    chunks = chunk_document(document=document, chunk_size=4, overlap=2)

    assert [chunk.text for chunk in chunks] == [
        "one two three four",
        "three four five six",
        "five six seven",
    ]


def test_chunk_documents_preserves_document_order() -> None:
    documents = [
        Document(document_id="doc-1", text="one two three four"),
        Document(document_id="doc-2", text="five six seven eight"),
    ]

    chunks = chunk_documents(documents=documents, chunk_size=2)

    assert [chunk.chunk_id for chunk in chunks] == [
        "doc-1::chunk-0",
        "doc-1::chunk-1",
        "doc-2::chunk-0",
        "doc-2::chunk-1",
    ]


@pytest.mark.parametrize(
    ("chunk_size", "overlap"),
    [
        (0, 0),
        (-1, 0),
        (3, -1),
        (3, 3),
        (3, 4),
    ],
)
def test_chunk_document_rejects_invalid_chunking_args(
    chunk_size: int,
    overlap: int,
) -> None:
    document = Document(document_id="doc-1", text="one two three")

    with pytest.raises(ValueError):
        chunk_document(document=document, chunk_size=chunk_size, overlap=overlap)


def test_chunk_document_never_returns_empty_chunk_text() -> None:
    document = Document(document_id="doc-1", text="one two three")

    chunks = chunk_document(document=document, chunk_size=2, overlap=1)

    assert all(chunk.text for chunk in chunks)
