#!/usr/bin/env python3
"""Simple utility to query OpenAI Codex or compatible models.

Usage:
  python auto_codex.py "<prompt>"

Requires the environment variable OPENAI_API_KEY to be set.
"""
import json
import os
import sys
import urllib.request

API_URL = "https://api.openai.com/v1/chat/completions"
MODEL = "gpt-3.5-turbo"


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python auto_codex.py <prompt>", file=sys.stderr)
        return 1

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Environment variable OPENAI_API_KEY not set", file=sys.stderr)
        return 1

    prompt = sys.argv[1]
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "temperature": 0.2,
        "max_tokens": 200,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.load(resp)
    except Exception as e:
        print(f"Error calling OpenAI API: {e}", file=sys.stderr)
        return 1

    choices = result.get("choices")
    if choices:
        print(choices[0].get("text", "").strip())
        return 0
    else:
        print("No output", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
