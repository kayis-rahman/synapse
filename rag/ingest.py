import argparse
import os
import json
from rag.embedding import EmbeddingService
from rag.vectorstore import VectorStore

def chunk_text(text, chunk_size=500):
    """Split text into chunks of approximately chunk_size characters."""
    words = text.split()
    chunks = []
    current = ""
    for word in words:
        if len(current) + len(word) + 1 > chunk_size:
            if current:
                chunks.append(current.strip())
                current = word
            else:
                chunks.append(word)
        else:
            current += " " + word
    if current:
        chunks.append(current.strip())
    return chunks

def parse_tags(tags_str):
    """Parse tags string like 'project:pi-rag,service:docs' into dict."""
    tags = {}
    if tags_str:
        for pair in tags_str.split(','):
            if ':' in pair:
                key, value = pair.split(':', 1)
                tags[key.strip()] = value.strip()
    return tags

def ingest_file(file_path, tags, index_path='./rag_index'):
    """Ingest a single file into the vector store."""
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    chunks = chunk_text(text)
    if not chunks:
        print("No text to ingest.")
        return

    embedding_service = EmbeddingService()
    vectors = embedding_service.embed(chunks)

    metadata = [tags.copy() for _ in chunks]

    store = VectorStore(index_path)
    store.add(chunks, vectors, metadata)
    store.save()

    print(f"Ingested {len(chunks)} chunks from {file_path} with tags {tags}.")

def main():
    parser = argparse.ArgumentParser(description="Ingest codebase data into RAG memory.")
    parser.add_argument('--file', required=True, help="Path to file to ingest.")
    parser.add_argument('--tags', help="Tags in format key:value,key2:value2")
    parser.add_argument('--index-path', default='./rag_index', help="Path to vector store index.")

    args = parser.parse_args()
    tags = parse_tags(args.tags)
    ingest_file(args.file, tags, args.index_path)

if __name__ == "__main__":
    main()