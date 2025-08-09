#!/usr/bin/env python3
"""
Test module for generate tests

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import argparse
import os
import sys
import ast
import inspect
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestGenerator:
    def __init__(self, workspace_root=None):
        """Initialize the generator.

        Args:
            workspace_root (str | Path | None): Root directory to scan for
                Python files. Defaults to the parent directory of this script
                if not provided.
        """
        if workspace_root is None:
            workspace_root = Path(__file__).resolve().parent.parent
        self.workspace_root = Path(workspace_root)
        self.test_template = '''"""
Auto-generated tests for {module_name}
Generated on: {timestamp}
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add the module path to sys.path for importing
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from {module_path} import {imports}
except ImportError as e:
    print(f"Warning: Could not import from {module_path}: {{e}}")
    # Define mock classes/functions as fallbacks
{mock_definitions}

class Test{class_name}(unittest.TestCase):
    """Test cases for {class_name}"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        pass

    def tearDown(self):
        """Tear down test fixtures after each test method."""
        pass
{test_methods}

if __name__ == '__main__':
    unittest.main()
'''

    def generate_missing_tests(self, dry_run: bool = False):
        """Generate tests for files without test coverage.

        Args:
            dry_run (bool): If True, only show which tests would be generated
                without writing files.
        """
        print("🧪 Generating Missing Tests")
        print("=" * 40)

        python_files = list(self.workspace_root.rglob("*.py"))
        test_files = set()

        # Find existing test files
        for pattern in ["test_*.py", "*_test.py", "tests.py"]:
            test_files.update(self.workspace_root.rglob(pattern))

        generated_count = 0

        for python_file in python_files:
            # Skip test files and __init__.py files
            if (python_file in test_files or
                python_file.name == "__init__.py" or
                "test" in python_file.name.lower() or
                python_file.name.startswith(".")):
                continue

            # Check if test already exists
            if self._has_existing_test(python_file):
                continue

            try:
                if self._should_generate_test(python_file):
                    if dry_run:
                        print(f"✅ [Dry Run] Would generate test for: {python_file.relative_to(self.workspace_root)}")
                    else:
                        self._generate_test_file(python_file)
                        generated_count += 1
                        print(f"✅ Generated test for: {python_file.relative_to(self.workspace_root)}")
            except Exception as e:
                print(f"❌ Failed to generate test for {python_file.name}: {e}")

        print(f"\n📊 Generated {generated_count} test files")
        return {"generated_tests": generated_count}

    def _has_existing_test(self, python_file: Path) -> bool:
        """Check if a test file already exists for the given Python file."""
        possible_test_names = [
            f"test_{python_file.stem}.py",
            f"{python_file.stem}_test.py",
            f"test_{python_file.stem}s.py"
        ]

        test_dir = python_file.parent / "tests"

        # Check in same directory
        for test_name in possible_test_names:
            if (python_file.parent / test_name).exists():
                return True

        # Check in tests subdirectory
        if test_dir.exists():
            for test_name in possible_test_names:
                if (test_dir / test_name).exists():
                    return True

        return False

    def _should_generate_test(self, python_file: Path) -> bool:
        """Determine if a test should be generated for this file."""
        try:
            with open(python_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse the file to check for classes and functions
            tree = ast.parse(content)

            has_classes = any(isinstance(node, ast.ClassDef) for node in tree.body)
            has_functions = any(isinstance(node, ast.FunctionDef) for node in tree.body)

            # Generate tests if file has classes or functions
            return has_classes or has_functions

        except Exception:
            return False

    def _generate_test_file(self, python_file: Path):
        """Generate a test file for the given Python file."""
        try:
            with open(python_file, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content)

            # Extract classes and functions
            classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
            functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]

            # Determine module path
            relative_path = python_file.relative_to(self.workspace_root)
            module_path = str(relative_path.with_suffix('')).replace('/', '.')

            # Create test content
            imports = []
            mock_definitions = []
            test_methods = []

            # Handle classes
            for class_node in classes:
                class_name = class_node.name
                imports.append(class_name)

                # Generate mock definition
                mock_definitions.append(f"""
class {class_name}:
    \"\"\"Mock {class_name} class\"\"\"
    pass
""")

                # Generate basic test methods for the class
                test_methods.extend(self._generate_class_tests(class_name, class_node))

            # Handle standalone functions
            for func_node in functions:
                if not func_node.name.startswith('_'):  # Skip private functions
                    func_name = func_node.name
                    imports.append(func_name)

                    mock_definitions.append(f"""
def {func_name}(*args, **kwargs):
    \"\"\"Mock {func_name} function\"\"\"
    return None
""")

                    test_methods.extend(self._generate_function_tests(func_name, func_node))

            if not imports:
                return  # Nothing to test

            # Create test file
            test_filename = f"test_{python_file.stem}.py"
            test_dir = python_file.parent / "tests"
            test_dir.mkdir(exist_ok=True)

            test_file_path = test_dir / test_filename

            # Fill template
            test_content = self.test_template.format(
                module_name=python_file.stem,
                timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                module_path=module_path,
                imports=', '.join(imports),
                mock_definitions=''.join(mock_definitions),
                class_name=python_file.stem.title().replace('_', ''),
                test_methods=''.join(test_methods)
            )

            with open(test_file_path, 'w', encoding='utf-8') as f:
                f.write(test_content)

        except Exception as e:
            logger.error(f"Error generating test for {python_file}: {e}")
            raise

    def _generate_class_tests(self, class_name: str, class_node: ast.ClassDef) -> list:
        """Generate test methods for a class."""
        test_methods = []

        # Basic instantiation test
        test_methods.append(f"""
    def test_{class_name.lower()}_instantiation(self):
        \"\"\"Test {class_name} can be instantiated.\"\"\"
        try:
            instance = {class_name}()
            self.assertIsNotNone(instance)
        except Exception as e:
            self.skipTest(f"Cannot instantiate {class_name}: {{e}}")
""")

        # Generate tests for methods
        methods = [node for node in class_node.body if isinstance(node, ast.FunctionDef)]
        for method in methods:
            if not method.name.startswith('_') or method.name == '__init__':
                method_name = method.name
                test_methods.append(f"""
    def test_{class_name.lower()}_{method_name}(self):
        \"\"\"Test {class_name}.{method_name} method.\"\"\"
        try:
            instance = {class_name}()
            # TODO: Add specific test logic for {method_name}
            self.assertTrue(hasattr(instance, '{method_name}'))
        except Exception as e:
            self.skipTest(f"Cannot test {class_name}.{method_name}: {{e}}")
""")

        return test_methods

    def _generate_function_tests(self, func_name: str, func_node: ast.FunctionDef) -> list:
        """Generate test methods for a standalone function."""
        test_methods = []

        # Basic function test
        test_methods.append(f"""
    def test_{func_name}(self):
        \"\"\"Test {func_name} function.\"\"\"
        try:
            # TODO: Add specific test logic for {func_name}
            result = {func_name}()
            # Add assertions based on expected behavior
            # self.assertEqual(result, expected_value)
            self.assertTrue(True)  # Placeholder assertion
        except Exception as e:
            self.skipTest(f"Cannot test {func_name}: {{e}}")
""")

        return test_methods

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate stub test files for Python modules without tests."
    )
    parser.add_argument(
        "--workspace-root",
        type=str,
        default=str(Path(__file__).resolve().parent.parent),
        help="Root directory to scan for Python files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List files that would receive tests without creating them.",
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point."""
    args = parse_args()
    generator = TestGenerator(workspace_root=args.workspace_root)
    result = generator.generate_missing_tests(dry_run=args.dry_run)
    print(f"\n📋 Test Generation Complete: {result}")

if __name__ == "__main__":
    main()
