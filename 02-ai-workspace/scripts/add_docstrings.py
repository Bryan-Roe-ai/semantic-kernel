#!/usr/bin/env python3
"""
Add Docstrings
Automatically adds docstrings to undocumented functions and classes.
"""

import os
import sys
import ast
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocstringAdder:
    def __init__(self, workspace_root="/workspaces/semantic-kernel/ai-workspace"):
        self.workspace_root = Path(workspace_root)

    def add_missing_docstrings(self):
        """Add docstrings to undocumented functions and classes."""
        print("📝 Adding Missing Docstrings")
        print("=" * 40)

        python_files = list(self.workspace_root.rglob("*.py"))
        modified_files = 0
        total_additions = 0

        for python_file in python_files:
            # Skip test files and __init__.py files
            if (python_file.name.startswith("test_") or
                python_file.name.endswith("_test.py") or
                python_file.name == "__init__.py" or
                python_file.name.startswith(".")):
                continue

            try:
                additions = self._add_docstrings_to_file(python_file)
                if additions > 0:
                    modified_files += 1
                    total_additions += additions
                    print(f"✅ Added {additions} docstrings to: {python_file.relative_to(self.workspace_root)}")
            except Exception as e:
                print(f"❌ Failed to process {python_file.name}: {e}")

        print(f"\n📊 Added {total_additions} docstrings to {modified_files} files")
        return {"modified_files": modified_files, "total_additions": total_additions}

    def _add_docstrings_to_file(self, python_file: Path) -> int:
        """Add docstrings to a specific file."""
        try:
            with open(python_file, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content)
            lines = content.split('\n')

            additions = 0

            # Process classes and functions
            for node in ast.walk(tree):
                if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                    if not self._has_docstring(node):
                        docstring = self._generate_docstring(node)
                        if docstring:
                            # Insert docstring after the definition line
                            insert_line = node.lineno  # Line after def/class
                            indent = self._get_indent_level(lines[node.lineno - 1]) + 4

                            docstring_lines = [
                                ' ' * indent + '"""',
                                ' ' * indent + docstring,
                                ' ' * indent + '"""'
                            ]

                            # Insert the docstring
                            for i, doc_line in enumerate(docstring_lines):
                                lines.insert(insert_line + i, doc_line)

                            additions += 1

            if additions > 0:
                # Write the modified content back
                with open(python_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))

            return additions

        except Exception as e:
            logger.error(f"Error processing {python_file}: {e}")
            return 0

    def _has_docstring(self, node):
        """Check if a node already has a docstring."""
        if (hasattr(node, 'body') and
            node.body and
            isinstance(node.body[0], ast.Expr) and
            isinstance(node.body[0].value, ast.Str)):
            return True
        return False

    def _generate_docstring(self, node):
        """Generate an appropriate docstring for a node."""
        if isinstance(node, ast.ClassDef):
            return f"{node.name} class."
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith('_'):
                return f"Private method: {node.name}."
            elif node.name == '__init__':
                return "Initialize the instance."
            else:
                return f"{node.name.replace('_', ' ').title()} function."
        return None

    def _get_indent_level(self, line: str) -> int:
        """Get the indentation level of a line."""
        return len(line) - len(line.lstrip())

def main():
    """Main function."""
    adder = DocstringAdder()
    result = adder.add_missing_docstrings()
    print(f"\n📋 Docstring Addition Complete: {result}")

if __name__ == "__main__":
    main()
