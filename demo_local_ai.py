#!/usr/bin/env python3
"""Deprecation shim for migrated sample.

Original content moved to: samples/local_ai/demo_local_ai.py
This shim will be removed after 2025-12-31.
"""
from __future__ import annotations

import importlib
import sys

TARGET = "samples.local_ai.demo_local_ai"


def main():  # pragma: no cover - trivial wrapper
    print("[DEPRECATION] 'demo_local_ai.py' moved to 'samples/local_ai/demo_local_ai.py'.\n"
          "Use: python -m samples.local_ai.demo_local_ai (shim removed after 2025-12-31).")
    mod = importlib.import_module(TARGET)
    if hasattr(mod, "main"):
        mod.main()
    else:  # Fallback if structure changes
        if hasattr(mod, "__dict__"):
            print("[INFO] Target module imported; no main() found.")


if __name__ == "__main__":
    sys.exit(main())
