import argparse
import json
import os
import hashlib
from pathlib import Path
from rag.embedding import EmbeddingService
from rag.vectorstore import VectorStore

def compute_file_hash(file_path):
    """Compute SHA256 hash of file content."""
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def should_skip_file(file_path, exclusions):
    """Check if file should be skipped based on exclusions."""
    path = Path(file_path)
    for exclusion in exclusions:
        if exclusion in str(path) or path.match(exclusion):
            return True
    return False

def infer_tags(file_path, tag_mappings):
    """Infer tags from file path using mappings."""
    tags = {}
    path_str = str(file_path).lower()
    for key, value in tag_mappings.items():
        if key.lower() in path_str:
            tags.update(value)
    return tags

def chunk_text(text, chunk_size=500):
    """Split text into chunks."""
    words = text.split()
    chunks = []
    current = ""
    for word in words:
        if len(current) + len(word) + 1 > chunk_size:
            if current:
                chunks.append(current.strip())
            current = word
        else:
            current += " " + word
    if current:
        chunks.append(current.strip())
    return chunks

def load_config(config_path):
    """Load config from JSON file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file {config_path} not found.")
    with open(config_path, 'r') as f:
        return json.load(f)

def process_file(file_path, config, store, update_mode=False):
    """Process a single file: check hash, chunk, embed, store."""
    file_hash = compute_file_hash(file_path)
    file_meta_key = {"file_path": str(file_path)}

    # Check if file changed (for update mode)
    if update_mode:
        for meta in store.metadata:
            if meta.get("file_path") == str(file_path):
                if meta.get("file_hash") == file_hash:
                    print(f"Skipping unchanged file: {file_path}")
                    return
                break

    # Remove old entries for this file
    store.remove_by_metadata(file_meta_key)

    # Read and process
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    chunks = chunk_text(text, config.get("chunk_size", 500))
    if not chunks:
        return

    embedding_service = EmbeddingService()
    try:
        vectors = embedding_service.embed(chunks)
    except Exception as e:
        print(f"Embedding failed for {file_path}: {e}")
        return

    # Tags: project + inferred + file metadata
    tags = {"project": config["project"], "file_path": str(file_path), "file_hash": file_hash}
    tags.update(infer_tags(file_path, config.get("tag_mappings", {})))

    metadata = [tags.copy() for _ in chunks]

    store.add(chunks, vectors, metadata)
    print(f"Processed {len(chunks)} chunks from {file_path}")

def bulk_ingest(folder, config_path, update=False):
    """Bulk ingest from folder."""
    config = load_config(config_path)
    index_path = config.get("index_path", "./rag_index")
    exclusions = config.get("exclusions", ["__pycache__", ".git", "build", "*.pyc", "*.log"])
    file_types = set(config.get("file_types", [".py", ".md"]))

    store = VectorStore(index_path)
    store.load()

    folder_path = Path(folder)
    processed = 0

    for file_path in folder_path.rglob("*"):
        if file_path.is_file() and file_path.suffix in file_types and not should_skip_file(file_path, exclusions):
            try:
                process_file(file_path, config, store, update)
                processed += 1
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    store.save()
    print(f"Bulk ingestion complete: {processed} files processed.")

def main():
    parser = argparse.ArgumentParser(description="Bulk ingest codebase into RAG memory.")
    parser.add_argument('--folder', required=True, help="Root folder to scan.")
    parser.add_argument('--config', required=True, help="Path to config JSON.")
    parser.add_argument('--update', action='store_true', help="Incremental update mode.")

    args = parser.parse_args()
    bulk_ingest(args.folder, args.config, args.update)

if __name__ == "__main__":
    main()