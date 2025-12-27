#!/usr/bin/env python3
"""
Index all repository files into the RAG system.
"""

import os
import json
import requests
import re
from pathlib import Path

def chunk_text(text, chunk_size=500, chunk_overlap=50):
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - chunk_overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    
    return chunks

def should_skip_file(file_path):
    """Check if file should be skipped."""
    skip_patterns = [
        r'\.pyc$', r'\.pyo$', r'__pycache__', r'\.git',
        r'\.DS_Store', r'node_modules', r'\.venv', r'venv',
        r'build', r'dist', r'\.egg-info', r'chroma_db',
        r'\.cache', r'\.huggingface', r'\.cache', r'.aider*'
    ]
    
    for pattern in skip_patterns:
        if re.search(pattern, str(file_path), re.IGNORECASE):
            return True
    
    return False

def get_file_type(file_path):
    """Get file type for metadata."""
    ext = Path(file_path).suffix.lower()
    type_map = {
        '.py': 'python',
        '.md': 'markdown',
        '.txt': 'text',
        '.json': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.sh': 'shell',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.html': 'html',
        '.css': 'css',
        '.rst': 'rst',
        '.cfg': 'config',
        '.ini': 'config',
        '.toml': 'config'
    }
    return type_map.get(ext, 'text')

def ingest_file(file_path, api_url="http://localhost:8001/v1/ingest"):
    """Ingest a single file into the RAG system."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.strip():
            print(f"Skipping empty file: {file_path}")
            return 0
        
        chunks = chunk_text(content)
        total_chunks = 0
        
        for i, chunk in enumerate(chunks):
            payload = {
                "text": chunk,
                "source_name": f"{file_path} (chunk {i+1})",
                "chunk_size": 500,
                "chunk_overlap": 50,
                "metadata": {
                    "project": "pi-rag",
                    "type": "repo",
                    "file_type": get_file_type(file_path),
                    "file_path": str(file_path),
                    "chunk_index": i + 1,
                    "total_chunks": len(chunks)
                }
            }
            
            response = requests.post(api_url, json=payload)
            if response.status_code == 200:
                total_chunks += 1
            else:
                print(f"Error ingesting {file_path} chunk {i+1}: {response.text}")
        
        return total_chunks
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0

def main():
    """Main function to index repository."""
    api_url = "http://localhost:8001/v1/ingest"
    
    # Get all files in the repository
    repo_files = []
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            file_path = os.path.join(root, file)
            if not should_skip_file(file_path):
                repo_files.append(file_path)
    
    print(f"Found {len(repo_files)} files to index")
    
    total_chunks = 0
    processed_files = 0
    
    for i, file_path in enumerate(repo_files, 1):
        print(f"[{i}/{len(repo_files)}] Processing: {file_path}")
        chunks = ingest_file(file_path, api_url)
        if chunks > 0:
            total_chunks += chunks
            processed_files += 1
    
    print(f"\nIndexing Complete!")
    print(f"Files processed: {processed_files}/{len(repo_files)}")
    print(f"Total chunks created: {total_chunks}")

if __name__ == "__main__":
    main()