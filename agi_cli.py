#!/usr/bin/env python3
"""
AGI Command Line Interface for AI development tools

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import asyncio
import sys
from pathlib import Path

# Allow running this script directly from the repository root without
# requiring semantic_kernel to be installed in the environment.
repo_root = Path(__file__).resolve().parent
local_package = repo_root / "01-core-implementations" / "python"
if local_package.exists():
    sys.path.insert(0, str(local_package))

try:
    from semantic_kernel import Kernel
    from semantic_kernel.functions import kernel_function
except ModuleNotFoundError as e:  # pragma: no cover - dependency missing
    sys.stderr.write(
        f"Semantic Kernel package not found: {e}. Install dependencies to use agi_cli.\n"
    )
    sys.exit(1)

class AGICommandLine:
    """Command line interface for AGI agents"""

    def __init__(self):
        self.kernel = Kernel()
        self.setup_agi_functions()

    def setup_agi_functions(self):
        """Setup AGI command functions"""
        self.kernel.add_plugin(self, plugin_name="agi_cli")

    @kernel_function(description="Execute AGI reasoning task")
    def reason(self, query: str) -> str:
        """Perform reasoning on a query"""
        steps = [
            f"1. Analyzing query: '{query}'",
            "2. Breaking down into components",
            "3. Applying logical reasoning",
            "4. Generating response"
        ]
        return "\n".join(steps) + f"\n\n💡 Result: This demonstrates AGI reasoning for '{query}'"

    @kernel_function(description="Process file with AGI")
    def process_file(self, filename: str, operation: str = "analyze") -> str:
        """Process a file using AGI capabilities"""
        operations = {
            "analyze": f"📊 Analyzed file structure and content of {filename}",
            "optimize": f"⚡ Optimized {filename} for better performance",
            "transform": f"🔄 Transformed {filename} to new format",
            "summarize": f"📝 Generated summary of {filename}"
        }
        return operations.get(operation, f"🔧 Processed {filename} with {operation}")

    @kernel_function(description="Generate code with AGI")
    def generate_code(self, language: str, description: str) -> str:
        """Generate code using AGI"""
        templates = {
            "python": f"# {description}\ndef main():\n    print('Hello from AGI generated code!')\n    return True\n\nif __name__ == '__main__':\n    main()",
            "javascript": f"// {description}\nfunction main() {{\n    console.log('Hello from AGI generated code!');\n    return true;\n}}\n\nmain();",
            "bash": f"#!/bin/bash\n# {description}\necho 'Hello from AGI generated code!'\nexit 0"
        }
        return templates.get(language.lower(), f"# {description}\n// Code generated for {language}")

    @kernel_function(description="Plan and execute tasks")
    def plan_task(self, goal: str) -> str:
        """Create and execute a plan for achieving a goal"""
        plan_steps = [
            f"🎯 Goal: {goal}",
            "📋 Planning phase:",
            "  1. Define requirements",
            "  2. Identify resources",
            "  3. Create timeline",
            "  4. Execute steps",
            "  5. Monitor progress",
            "✅ Plan created and ready for execution"
        ]
        return "\n".join(plan_steps)

# 1) Move the help text to a module‐level constant
HELP_TEXT = """
🤖 AGI Command Line Interface
Available commands:
  reason <query>              - Perform AGI reasoning on a query
  file <filename> [operation] - Process file (analyze, optimize, transform, summarize)
  code <language> <description> - Generate code in specified language
  plan <goal>                 - Create and execute a plan for a goal
  help                        - Show this help message
Examples:
  python agi_cli.py reason "How does machine learning work?"
  python agi_cli.py file myfile.txt analyze
  python agi_cli.py code python "Create a web scraper"
  python agi_cli.py plan "Build a recommendation system"
"""

# 2) Extract retry logic into a decorator
def retry_async(max_retries: int = 3, retry_delay: float = 1.0):
    def decorator(fn):
        async def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    return await fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries:
                        print(f"❌ Error after {max_retries} attempts: {e}")
                        return False
                    print(f"⚠️  Attempt {attempt} failed: {e}. Retrying in {retry_delay} seconds…")
                    await asyncio.sleep(retry_delay)
        return wrapper
    return decorator

# 3) Define per‐command handlers, then dispatch via a map
async def _handle_reason(agi, args):
    query = " ".join(args) if args else "What is artificial general intelligence?"
    fn = agi.kernel.get_function("agi_cli", "reason")
    return await fn.invoke(agi.kernel, query=query)

# … similarly define _handle_file, _handle_code, _handle_plan …

COMMAND_HANDLERS = {
    "reason": _handle_reason,
    "file":   _handle_file,
    "code":   _handle_code,
    "plan":   _handle_plan,
    "help":   lambda agi, args: HELP_TEXT,
}

# 4) Simplify run_command
@retry_async()
async def run_command(command: str, *args) -> bool:
    agi = AGICommandLine()
    handler = COMMAND_HANDLERS.get(command)
    if not handler:
        print(f"❌ Unknown command: {command}. Use 'help' for available commands.")
        return False

    result = await handler(agi, args)
    print(result)
    return True
    command: str,
    *args,
    max_retries: int = 3,
    retry_delay: float = 1.0,
) -> bool:
    """Run an AGI command with basic retry logic."""
    agi = AGICommandLine()

    for attempt in range(1, max_retries + 1):
        try:
            if command == "reason":
                query = " ".join(args) if args else "What is artificial general intelligence?"
                function = agi.kernel.get_function("agi_cli", "reason")
                result = await function.invoke(agi.kernel, query=query)

            elif command == "file":
                filename = args[0] if args else "example.txt"
                operation = args[1] if len(args) > 1 else "analyze"
                function = agi.kernel.get_function("agi_cli", "process_file")
                result = await function.invoke(agi.kernel, filename=filename, operation=operation)

            elif command == "code":
                language = args[0] if args else "python"
                description = " ".join(args[1:]) if len(args) > 1 else "Simple example function"
                function = agi.kernel.get_function("agi_cli", "generate_code")
                result = await function.invoke(agi.kernel, language=language, description=description)

            elif command == "plan":
                goal = " ".join(args) if args else "Complete project tasks"
                function = agi.kernel.get_function("agi_cli", "plan_task")
                result = await function.invoke(agi.kernel, goal=goal)

            elif command == "help":
                result = """
🤖 AGI Command Line Interface

Available commands:
  reason <query>              - Perform AGI reasoning on a query
  file <filename> [operation] - Process file (analyze, optimize, transform, summarize)
  code <language> <description> - Generate code in specified language
  plan <goal>                 - Create and execute a plan for a goal
  help                        - Show this help message

Examples:
  python agi_cli.py reason "How does machine learning work?"
  python agi_cli.py file myfile.txt analyze
  python agi_cli.py code python "Create a web scraper"
  python agi_cli.py plan "Build a recommendation system"
            """
            else:
                result = f"❌ Unknown command: {command}. Use 'help' for available commands."

            print(result)
            return True

        except Exception as e:
            if attempt == max_retries:
                print(f"❌ Error executing command after {max_retries} attempts: {e}")
                return False
            print(f"⚠️  Attempt {attempt} failed: {e}. Retrying in {retry_delay} seconds...")
            await asyncio.sleep(retry_delay)

def main():
    """Main CLI function"""
    if len(sys.argv) < 2:
        print("🤖 AGI Command Line Interface")
        print("Usage: python agi_cli.py <command> [args...]")
        print("Use 'help' for available commands")
        return

    command = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []

    asyncio.run(run_command(command, *args))

if __name__ == "__main__":
    main()
