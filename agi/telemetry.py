"""Telemetry utilities: JSONL logging decorator."""
from __future__ import annotations
import json, time, functools, os
from typing import Callable, Any, Dict, Optional

LOG_PATH = os.environ.get("AGI_TELEMETRY_LOG", "agi_metrics.jsonl")

def telemetry(event_type: str, context_fn: Optional[Callable[..., Dict[str, Any]]] = None):
    """Decorator to log function execution metrics.

    context_fn: optional callable to derive additional context dict from args/kwargs.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            success = False
            try:
                result = func(*args, **kwargs)
                success = True
                return result
            except Exception as e:  # pragma: no cover - basic logging safety
                success = False
                raise e
            finally:
                duration = time.time() - start
                record: Dict[str, Any] = {
                    "event": event_type,
                    "function": func.__name__,
                    "duration_ms": int(duration * 1000),
                    "success": success,
                }
                if context_fn:
                    try:  # pragma: no cover
                        extra = context_fn(*args, **kwargs) or {}
                        record.update(extra)
                    except Exception:
                        record["context_error"] = True
                with open(LOG_PATH, "a", encoding="utf-8") as f:
                    f.write(json.dumps(record) + "\n")
        return wrapper
    return decorator


def approximate_tokens(text: str) -> int:
    """Very rough token count approximation (~4 chars/token heuristic)."""
    if not text:
        return 0
    return max(1, len(text) // 4)
