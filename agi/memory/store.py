"""Simple in-process memory store (placeholder).
Not optimized; provides interface consistent with future vector-backed plugin.

Vector Similarity Strategy:
- If AGI_FEATURE_FLAGS includes 'semantic_memory' and sentence_transformers is available: use real MiniLM embeddings.
- Else: deterministic hash bucket embedding + cosine.
- Secondary fallback: token overlap heuristic when vector score is zero.
- Upgrade Path: allow model selection via environment variable in future without API break.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any
import math, hashlib, os
import threading
from agi.flags import enabled

@dataclass
class MemoryItem:
    id: str
    text: str
    metadata: Dict[str, Any]

class MemoryStore:
    def __init__(self):
        self._items: Dict[str, MemoryItem] = {}
        self._embedder = None
    self._embedder_lock = threading.Lock()
    # Simple in-memory embedding vector cache
    self._vector_cache = {}

    def _maybe_load_embedder(self):  # lazy load to avoid import cost when unused
        if self._embedder is not None:
            return
        with self._embedder_lock:
            if self._embedder is not None:
                return
            try:
                from sentence_transformers import SentenceTransformer  # type: ignore
                model_name = os.environ.get("AGI_EMBEDDING_MODEL", "all-MiniLM-L6-v2")
                self._embedder = SentenceTransformer(model_name)
            except Exception:
                self._embedder = None

    def upsert(self, item: MemoryItem) -> None:
        self._items[item.id] = item

    def get(self, item_id: str) -> MemoryItem | None:
        return self._items.get(item_id)

    def delete(self, item_id: str) -> bool:
        return self._items.pop(item_id, None) is not None

    def _text_to_vector(self, text: str, dims: int = 16) -> List[float]:
        cached = self._vector_cache.get(text)
        if cached is not None:
            return cached
        # If semantic flag enabled and embedder available, use real embeddings; else hash buckets.
        if enabled("semantic_memory"):
            self._maybe_load_embedder()
            if self._embedder is not None:
                try:
                    vec = self._embedder.encode([text])[0]
                    # Normalize
                    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
                    out = [float(x / norm) for x in vec]
                    self._vector_cache[text] = out
                    return out
                except Exception:
                    pass
        # Fallback deterministic embedding via hashing
        vec2 = [0.0] * dims
        for i, token in enumerate(text.lower().split()):
            h = int(hashlib.sha256(token.encode()).hexdigest(), 16)
            vec2[h % dims] += 1.0
            if i > 256:
                break
        norm2 = math.sqrt(sum(x * x for x in vec2)) or 1.0
        out2 = [x / norm2 for x in vec2]
        self._vector_cache[text] = out2
        return out2

    def _cosine(self, a: List[float], b: List[float]) -> float:
        return sum(x * y for x, y in zip(a, b))

    def similar(self, query: str, k: int = 5) -> List[tuple[MemoryItem, float]]:
        # Two-tier approach: hashed vector cosine as primary; fallback to token overlap if zero.
        use_semantic = enabled("semantic_memory")
        q_vec = self._text_to_vector(query) if use_semantic else None
        q_tokens = set(query.lower().split())
        scored: List[tuple[MemoryItem, float]] = []
        for it in self._items.values():
            cosine = 0.0
            if use_semantic and q_vec is not None:
                v = self._text_to_vector(it.text)
                cosine = self._cosine(q_vec, v)
            if cosine == 0 and q_tokens:
                it_tokens = set(it.text.lower().split())
                overlap = len(q_tokens & it_tokens)
                cosine = overlap / math.sqrt(len(q_tokens) * (len(it_tokens) or 1)) if q_tokens else 0.0
            if cosine > 0:
                scored.append((it, cosine))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:k]

    def list(self) -> List[MemoryItem]:
        return list(self._items.values())
