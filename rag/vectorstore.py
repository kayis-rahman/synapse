import json
import os

from typing import List, Dict, Optional, Tuple

import numpy as np


class VectorStore:
    def __init__(self, index_path=None):
        self.index_path = index_path
        self.docs = []
        self.vectors = []
        self.metadata = []
        if index_path and os.path.exists(index_path):
            self.load(index_path)

    def add(self, docs, vectors, metadata=None):
        if len(docs) != len(vectors):
            raise ValueError("docs and vectors length mismatch")
        self.docs.extend(docs)
        self.vectors.extend(vectors)
        if metadata is not None:
            if len(metadata) != len(docs):
                raise ValueError("metadata length must match docs length")
            self.metadata.extend(metadata)
        else:
            self.metadata.extend([{} for _ in docs])

    def _cosine(self, a, b):
        if not a or not b:
            return 0.0
        dot = sum(x * y for x, y in zip(a, b))
        na = sum(x * x for x in a) ** 0.5
        nb = sum(x * x for x in b) ** 0.5
        if na == 0 or nb == 0:
            return 0.0
        return dot / (na * nb)

    def search(self, query_vector, top_k=5):
        if not self.vectors:
            return []
        scores = []
        for i, vec in enumerate(self.vectors):
            s = self._cosine(query_vector, vec)
            scores.append((i, s))
        scores.sort(key=lambda x: x[1], reverse=True)
        results = []
        for idx, score in scores[:top_k]:
            results.append((self.docs[idx], score, self.metadata[idx]))
        return results

    def save(self, path=None):
        target = path or self.index_path
        if not target:
            raise ValueError("target path required to save index")
        os.makedirs(target, exist_ok=True)
        np.save(os.path.join(target, 'vectors.npy'), np.array(self.vectors, dtype=float))
        with open(os.path.join(target, 'docs.json'), 'w', encoding='utf-8') as f:
            json.dump(self.docs, f, ensure_ascii=False)
        with open(os.path.join(target, 'meta.json'), 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False)

    def load(self, path=None):
        target = path or self.index_path
        if not target or not os.path.exists(target):
            return
        docs_file = os.path.join(target, 'docs.json')
        vectors_file = os.path.join(target, 'vectors.npy')
        meta_file = os.path.join(target, 'meta.json')
        if not os.path.exists(docs_file) or not os.path.exists(vectors_file) or not os.path.exists(meta_file):
            return
        with open(docs_file, 'r', encoding='utf-8') as f:
            self.docs = json.load(f)
        vectors = np.load(vectors_file)
        self.vectors = vectors.tolist()
        with open(meta_file, 'r', encoding='utf-8') as f:
            self.metadata = json.load(f)
