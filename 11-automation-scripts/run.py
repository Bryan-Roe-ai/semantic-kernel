#!/usr/bin/env python3
"""DEPRECATION SHIM: run.py moved to scripts/run.py"""
import importlib
print("[DEPRECATED] run.py moved to scripts/run.py")
impl = importlib.import_module('scripts.run')
if __name__ == '__main__':
    impl.main()
