#!/usr/bin/env python3
"""Lightweight test script for llm_config model selection & fallback.
Run: python tests/test_llm_config_fallback.py
"""
import os
import json
from pathlib import Path
import sys
from llm_config_loader import load_llm_config_with_preview_control

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Minimal copy of helper to avoid heavy imports (no httpx needed)

    # Use shared loader for all test logic

CONFIG_PATH = ROOT / 'llm_config.json'


def _load_jsonc(path: Path):
    raw = path.read_text(encoding='utf-8')
    out_lines = []
    for line in raw.splitlines():
        stripped = line.lstrip()
        if stripped.startswith('//'):
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
            elif not in_string and ch == '/' and i+1 < len(line) and line[i+1] == '/':
                # comment start outside string -> stop processing line
                break
            else:
                new_line.append(ch)
            escape = (ch == '\\' and not escape)
            if ch != '\\':
                # reset escape if current char isn't backslash
                escape = False if ch != '"' else escape
            i += 1
        candidate = ''.join(new_line).rstrip()
        if candidate:
            out_lines.append(candidate)
    cleaned = '\n'.join(out_lines)
    return json.loads(cleaned)


def write_temp_config(models_override=None, preferred_override=None):
    base = _load_jsonc(CONFIG_PATH)
    if models_override:
        base['models'] = models_override
    if preferred_override:
        base['preferred_chat_models'] = preferred_override
    tmp = ROOT / 'llm_config.test.json'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(base, f, indent=2)
    return tmp


def test_preferred_first_enabled():
    tmp = write_temp_config()
    for v in ['OPENAI_CHAT_MODEL_ID','OPENAI_MODEL','DISABLE_PREVIEW_MODELS']:
        os.environ.pop(v, None)
    cfg = load_llm_config_with_preview_control(tmp)
    assert cfg['active_chat_model'] == cfg['preferred_chat_models_effective'][0], 'Should pick first preferred model'


def test_disable_preview_removes_first():
    tmp = write_temp_config()
    os.environ['DISABLE_PREVIEW_MODELS'] = 'true'
    for v in ['OPENAI_CHAT_MODEL_ID','OPENAI_MODEL']:
        os.environ.pop(v, None)
    cfg = load_llm_config_with_preview_control(tmp)
    assert cfg['preferred_chat_models_effective'][0] != 'gpt-5-preview', 'Preview should be removed when disabled'


def test_env_override():
    tmp = write_temp_config()
    os.environ['OPENAI_CHAT_MODEL_ID'] = 'gpt-4o'
    cfg = load_llm_config_with_preview_control(tmp)
    assert cfg['active_chat_model'] == 'gpt-4o', 'Env override should force model'


def test_fallback_traversal_when_first_disabled():
    # Copy config and mark first preview model disabled; ensure next enabled chosen.
    base = _load_jsonc(CONFIG_PATH)
    base['models']['gpt-5-preview']['enabled'] = False
    tmp = ROOT / 'llm_config.test.json'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(base, f, indent=2)
    for v in ['OPENAI_CHAT_MODEL_ID','OPENAI_MODEL','DISABLE_PREVIEW_MODELS']:
        os.environ.pop(v, None)
    cfg = load_llm_config_with_preview_control(tmp)
    assert cfg['active_chat_model'] == 'gpt-4.1', 'Should skip disabled first preview and pick gpt-4.1'


def main():
    failures = 0
    for fn in [test_preferred_first_enabled, test_disable_preview_removes_first, test_env_override, test_fallback_traversal_when_first_disabled]:
        try:
            fn()
            print(f'[PASS] {fn.__name__}')
        except AssertionError as e:
            failures += 1
            print(f'[FAIL] {fn.__name__}: {e}')
    if failures:
        print(f'Failures: {failures}')
        sys.exit(1)
    print('All fallback tests passed.')

if __name__ == '__main__':
    main()
