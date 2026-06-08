from pathlib import Path

import pytest

from simple_rag_serving.documents import Document, load_documents


def write_jsonl(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines), encoding="utf-8")


def test_load_documents_reads_multiple_records(tmp_path: Path) -> None:
    path = tmp_path / "documents.jsonl"
    write_jsonl(
        path,
        [
            '{"document_id": "doc-1", "text": "First document.", "metadata": {"topic": "one"}}',
            '{"document_id": "doc-2", "text": "Second document.", "metadata": {"topic": "two"}}',
        ],
    )

    documents = load_documents(path)

    assert documents == [
        Document(
            document_id="doc-1",
            text="First document.",
            metadata={"topic": "one"},
        ),
        Document(
            document_id="doc-2",
            text="Second document.",
            metadata={"topic": "two"},
        ),
    ]


def test_load_documents_defaults_omitted_metadata(tmp_path: Path) -> None:
    path = tmp_path / "documents.jsonl"
    write_jsonl(path, ['{"document_id": "doc-1", "text": "Document text."}'])

    documents = load_documents(path)

    assert documents[0].metadata == {}


def test_load_documents_ignores_blank_lines(tmp_path: Path) -> None:
    path = tmp_path / "documents.jsonl"
    write_jsonl(
        path,
        [
            "",
            '{"document_id": "doc-1", "text": "Document text."}',
            "   ",
        ],
    )

    documents = load_documents(path)

    assert len(documents) == 1


def test_load_documents_rejects_blank_document_id_with_line_number(
    tmp_path: Path,
) -> None:
    path = tmp_path / "documents.jsonl"
    write_jsonl(path, ['{"document_id": "   ", "text": "Document text."}'])

    with pytest.raises(ValueError, match="line 1"):
        load_documents(path)


def test_load_documents_rejects_blank_text_with_line_number(tmp_path: Path) -> None:
    path = tmp_path / "documents.jsonl"
    write_jsonl(path, ['{"document_id": "doc-1", "text": "   "}'])

    with pytest.raises(ValueError, match="line 1"):
        load_documents(path)


def test_load_documents_rejects_invalid_json_with_line_number(
    tmp_path: Path,
) -> None:
    path = tmp_path / "documents.jsonl"
    write_jsonl(path, ['{"document_id": "doc-1", "text":'])

    with pytest.raises(ValueError, match="line 1"):
        load_documents(path)


def test_load_documents_missing_file_raises_file_not_found(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_documents(tmp_path / "missing.jsonl")


def test_example_documents_file_loads() -> None:
    documents = load_documents(Path("data/examples/documents.jsonl"))

    assert 3 <= len(documents) <= 5
    assert all(document.document_id for document in documents)
    assert all(document.text for document in documents)
