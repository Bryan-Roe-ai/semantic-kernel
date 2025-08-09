"""
llm_config_loader.py

Unified loader for llm_config.json with preview disable and environment override logic.
Used by enhanced_ai_runner.py, ai_markdown_runner.py, and automation scripts.
"""
import os
import json
from pathlib import Path
from typing import Dict, Any

def load_llm_config_with_preview_control(config_path: Path) -> Dict[str, Any]:
    """
    Loads llm_config.json with support for:
    - JSONC (// comment) stripping
    - DISABLE_PREVIEW_MODELS env var
    - OPENAI_CHAT_MODEL_ID/OPENAI_MODEL override
    Returns dict with 'active_chat_model' and 'preferred_chat_models_effective'.
    """
    cfg: Dict[str, Any] = {}
    if config_path.exists():
        raw = config_path.read_text(encoding="utf-8")
        out_lines = []
        for line in raw.splitlines():
            stripped = line.lstrip()
            if stripped.startswith("//"):
                continue
            new_line = []
            in_string = False
            escape = False
            i = 0
            while i < len(line):
                ch = line[i]
                if ch == '"' and not escape:
                    in_string = not in_string
                    new_line.append(ch)
                elif not in_string and ch == '/' and i + 1 < len(line) and line[i+1] == '/':
                    break
                else:
                    new_line.append(ch)
                escape = (ch == '\\' and not escape)
                if ch != '\\':
                    escape = False if ch != '"' else escape
                i += 1
            candidate = ''.join(new_line).rstrip()
            if candidate:
                out_lines.append(candidate)
        cleaned = "\n".join(out_lines)
        try:
            if cleaned.strip():
                cfg = json.loads(cleaned)
        except Exception:
            pass
    env_override = os.environ.get("OPENAI_CHAT_MODEL_ID") or os.environ.get("OPENAI_MODEL")
    disable_preview = os.environ.get("DISABLE_PREVIEW_MODELS", "").lower() in ("1", "true", "yes")
    preferred = cfg.get("preferred_chat_models", [])
    metadata = cfg.get("models", {})
    if disable_preview:
        preferred = [m for m in preferred if not (m.endswith("-preview") or metadata.get(m, {}).get("status") == "preview")]
    if env_override:
        active = env_override
    else:
        active = None
        for mid in preferred:
            meta = metadata.get(mid)
            if not meta:
                active = mid
                break
            if not meta.get("enabled", True):
                continue
            active = mid
            break
    cfg["active_chat_model"] = env_override or active or cfg.get("active_chat_model")
    cfg["preferred_chat_models_effective"] = preferred
    return cfg
