from typing import List
import hashlib
try:
    from sentence_transformers import SentenceTransformer
except Exception:
    SentenceTransformer = None


class EmbeddingService:
    def __init__(self, model_name='all-MiniLM-L6-v2', use_cache=True):
        self.model_name = model_name
        self.use_cache = use_cache
        self._cache = {}
        self._model = None
        if SentenceTransformer is not None:
            try:
                self._model = SentenceTransformer(model_name)
            except Exception:
                self._model = None

    def embed(self, texts, batch_size=32):
        vectors = []
        uncached_texts = []
        uncached_indices = []
        for i, t in enumerate(texts):
            if self.use_cache and t in self._cache:
                vectors.append(self._cache[t])
            else:
                uncached_texts.append(t)
                uncached_indices.append(i)
                vectors.append(None)  # Placeholder

        if uncached_texts:
            if self._model is not None:
                try:
                    # Batch encode
                    batch_vectors = self._model.encode(uncached_texts, batch_size=batch_size, convert_to_numpy=True).tolist()
                    for idx, vec in zip(uncached_indices, batch_vectors):
                        if self.use_cache:
                            self._cache[texts[idx]] = vec
                        vectors[idx] = vec
                except Exception:
                    pass  # Fall back to individual

            # Fallback for any failures
            for i in uncached_indices:
                if vectors[i] is None:
                    vec = self._fallback_embed(texts[i])
                    if self.use_cache:
                        self._cache[texts[i]] = vec
                    vectors[i] = vec

        return vectors

    def _fallback_embed(self, text, dim=128):
        # Deterministic, lightweight fallback embedding based on hash
        h = hashlib.sha256(text.encode('utf-8')).hexdigest()
        nums = [int(h[i:i+8], 16) for i in range(0, len(h), 8)]
        vec = []
        for i in range(dim):
            val = nums[i % len(nums)]
            vec.append((val / float(2**32)) * 2.0 - 1.0)
        norm = sum(x * x for x in vec) ** 0.5
        if norm == 0:
            return [0.0 for _ in vec]
        return [x / norm for x in vec]
