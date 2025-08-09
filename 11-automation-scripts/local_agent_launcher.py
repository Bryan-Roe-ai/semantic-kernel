#!/usr/bin/env python3
"""Deprecation shim – moved to scripts/local_agent_launcher.py

This thin wrapper will be removed after 2025-12-31.
"""
from importlib import import_module
import sys

print("[DEPRECATION] Use 'python -m scripts.local_agent_launcher' instead (legacy shim).", file=sys.stderr)
_impl = import_module("scripts.local_agent_launcher")

if __name__ == "__main__":  # pragma: no cover - trivial delegation
    if hasattr(_impl, "main"):
        _impl.main()
    else:  # Fallback safety
        print("Target module has no main() function.", file=sys.stderr)
