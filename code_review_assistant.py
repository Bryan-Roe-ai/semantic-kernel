#!/usr/bin/env python3
"""
Code Review Assistant - A practical Semantic Kernel application.

This assistant helps review code by analyzing files and providing suggestions.
"""

import asyncio
import argparse
from pathlib import Path
from typing import Annotated

from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.ollama import OllamaChatCompletion
from semantic_kernel.functions import kernel_function


class CodeReviewPlugin:
    """Plugin for reading and analyzing code files."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root.resolve()

    @kernel_function(
        name="read_file", description="Read the contents of a source code file"
    )
    def read_file(
        self, file_path: Annotated[str, "Path to the file relative to repo root"]
    ) -> Annotated[str, "Contents of the file"]:
        """Read a file from the repository."""
        try:
            full_path = (self.repo_root / file_path).resolve()
            # Security check
            full_path.relative_to(self.repo_root)

            if not full_path.is_file():
                return f"Error: '{file_path}' is not a file"

            # Limit file size
            if full_path.stat().st_size > 100_000:
                return f"Error: File '{file_path}' is too large (>100KB)"

            content = full_path.read_text(encoding="utf-8")
            return f"File: {file_path}\n\n{content}"
        except Exception as e:
            return f"Error reading '{file_path}': {str(e)}"

    @kernel_function(
        name="list_python_files", description="List all Python files in a directory"
    )
    def list_python_files(
        self, directory: Annotated[str, "Directory path relative to repo root"] = "."
    ) -> Annotated[str, "List of Python files"]:
        """List Python files in a directory."""
        try:
            dir_path = (self.repo_root / directory).resolve()
            dir_path.relative_to(self.repo_root)

            if not dir_path.is_dir():
                return f"Error: '{directory}' is not a directory"

            python_files = sorted(
                [
                    str(f.relative_to(self.repo_root))
                    for f in dir_path.rglob("*.py")
                    if f.is_file()
                ]
            )

            if not python_files:
                return f"No Python files found in '{directory}'"

            return "\n".join(python_files[:50])  # Limit to 50 files
        except Exception as e:
            return f"Error listing files in '{directory}': {str(e)}"


async def run_code_review(file_path: str, repo_root: Path, model: str = "llama3.2"):
    """Run a code review on a specific file."""

    print(f"\n{'='*70}")
    print(f"🔍 Code Review Assistant")
    print(f"{'='*70}\n")

    # Setup kernel
    kernel = Kernel()
    service_id = "ollama"
    kernel.add_service(
        OllamaChatCompletion(
            service_id=service_id,
            ai_model_id=model,
            host="http://localhost:11434",
        )
    )

    # Add code review plugin
    kernel.add_plugin(CodeReviewPlugin(repo_root), plugin_name="code_tools")

    # Create reviewer agent
    agent = ChatCompletionAgent(
        kernel=kernel,
        name="CodeReviewer",
        instructions="""You are an expert code reviewer. When reviewing code:
1. Read the file using the read_file function
2. Analyze for:
   - Code quality and best practices
   - Potential bugs or security issues
   - Performance concerns
   - Readability and maintainability
3. Provide specific, actionable feedback
4. Be concise but thorough""",
        function_choice_behavior=FunctionChoiceBehavior.Auto(),
    )

    # Request review
    review_request = f"Please review the code in '{file_path}' and provide feedback."
    print(f"📝 Request: {review_request}\n")
    print("🤖 Reviewing...\n")

    try:
        response = await agent.get_response(messages=review_request)
        print(f"📋 Review Results:\n")
        print(response.message)
        print(f"\n{'='*70}\n")
    except Exception as e:
        print(f"❌ Error during review: {e}\n")
        import traceback

        traceback.print_exc()


async def interactive_mode(repo_root: Path, model: str = "llama3.2"):
    """Run in interactive mode for multiple reviews."""

    print(f"\n{'='*70}")
    print(f"🔍 Code Review Assistant - Interactive Mode")
    print(f"{'='*70}\n")
    print("Commands:")
    print("  review <file>  - Review a specific file")
    print("  list [dir]     - List Python files in directory")
    print("  exit           - Exit the assistant\n")

    # Setup kernel
    kernel = Kernel()
    service_id = "ollama"
    kernel.add_service(
        OllamaChatCompletion(
            service_id=service_id,
            ai_model_id=model,
            host="http://localhost:11434",
        )
    )

    # Add plugin
    kernel.add_plugin(CodeReviewPlugin(repo_root), plugin_name="code_tools")

    # Create agent
    agent = ChatCompletionAgent(
        kernel=kernel,
        name="CodeReviewer",
        instructions="""You are an expert code reviewer with access to code reading tools.
When asked to review code, use the read_file function first, then analyze it.
Provide specific, actionable feedback on code quality, bugs, and improvements.""",
        function_choice_behavior=FunctionChoiceBehavior.Auto(),
    )

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                print("\n👋 Goodbye!\n")
                break

            print("\n🤖 Assistant: ", end="", flush=True)
            response = await agent.get_response(messages=user_input)
            print(f"{response.message}\n")

        except EOFError:
            print("\n\n👋 Goodbye!\n")
            break
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="AI-powered code review assistant using Semantic Kernel"
    )
    parser.add_argument(
        "file", nargs="?", help="File to review (omit for interactive mode)"
    )
    parser.add_argument(
        "--repo-root", type=Path, default=Path.cwd(), help="Repository root directory"
    )
    parser.add_argument("--model", default="llama3.2", help="Ollama model to use")
    parser.add_argument(
        "--interactive", "-i", action="store_true", help="Run in interactive mode"
    )

    args = parser.parse_args()

    if args.interactive or not args.file:
        asyncio.run(interactive_mode(args.repo_root, args.model))
    else:
        asyncio.run(run_code_review(args.file, args.repo_root, args.model))


if __name__ == "__main__":
    main()
