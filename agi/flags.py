"""Simple feature flags using environment variable AGI_FEATURE_FLAGS (comma-separated)."""
from __future__ import annotations
import os
from functools import lru_cache

ENV_VAR = "AGI_FEATURE_FLAGS"

@lru_cache(maxsize=1)
def _get_flags() -> set[str]:
    raw = os.environ.get(ENV_VAR, "")
    return {f.strip().lower() for f in raw.split(',') if f.strip()}

def enabled(flag: str) -> bool:
    return flag.lower() in _get_flags()
