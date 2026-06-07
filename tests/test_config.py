from pathlib import Path

import pytest
from pydantic import ValidationError

from simple_rag_serving.config import RagConfig


def test_rag_config_uses_expected_defaults() -> None:
    config = RagConfig()

    assert config.embedding_model_name == "intfloat/multilingual-e5-large-instruct"
    assert config.generation_model_name == "facebook/opt-125m"
    assert config.documents_path == Path("data/examples/documents.jsonl")


def test_rag_config_accepts_custom_values() -> None:
    config = RagConfig(
        embedding_model_name="custom-embedding-model",
        generation_model_name="custom-generation-model",
        documents_path=Path("data/custom/documents.jsonl"),
    )

    assert config.embedding_model_name == "custom-embedding-model"
    assert config.generation_model_name == "custom-generation-model"
    assert config.documents_path == Path("data/custom/documents.jsonl")


def test_rag_config_rejects_blank_embedding_model_name() -> None:
    with pytest.raises(ValidationError):
        RagConfig(embedding_model_name="   ")


def test_rag_config_rejects_blank_generation_model_name() -> None:
    with pytest.raises(ValidationError):
        RagConfig(generation_model_name="   ")


def test_rag_config_rejects_blank_documents_path() -> None:
    with pytest.raises(ValidationError):
        RagConfig(documents_path="")


def test_rag_config_documents_path_is_path() -> None:
    config = RagConfig(documents_path="data/examples/documents.jsonl")

    assert isinstance(config.documents_path, Path)
