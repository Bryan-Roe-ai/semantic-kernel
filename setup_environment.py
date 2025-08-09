#!/usr/bin/env python3
"""DEPRECATION SHIM: setup_environment.py moved to tools/environment/setup_environment.py"""
import importlib, sys
print("[DEPRECATED] setup_environment.py moved to tools/environment/setup_environment.py")
module = importlib.import_module('tools.environment.setup_environment')
if __name__ == '__main__':
    module.main()
