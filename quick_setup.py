#!/usr/bin/env python3
"""DEPRECATION SHIM: quick_setup.py moved to tools/environment/quick_setup.py"""
import importlib
print("[DEPRECATED] quick_setup.py moved to tools/environment/quick_setup.py")
impl = importlib.import_module('tools.environment.quick_setup')
if __name__ == '__main__':
    impl.main()
