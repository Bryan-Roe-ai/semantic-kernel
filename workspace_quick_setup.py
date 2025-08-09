#!/usr/bin/env python3
"""DEPRECATION SHIM: workspace_quick_setup.py moved to tools/environment/workspace_quick_setup.py"""
import importlib
print("[DEPRECATED] workspace_quick_setup.py moved to tools/environment/workspace_quick_setup.py")
impl = importlib.import_module('tools.environment.workspace_quick_setup')
if __name__ == '__main__':
    impl.main()
