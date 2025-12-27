import pytest
from rag.ingest import ingest_file, ingest_text, chunk_text


def test_chunk_text():
    text = "This is a test sentence. This is another test sentence."
    chunks = chunk_text(text, chunk_size=20)
    assert len(chunks) > 0


def test_ingest_file():
    # Just check that the function exists and can be imported
    assert callable(ingest_file)


def test_ingest_text():
    # Just check that the function exists and can be imported
    assert callable(ingest_text)