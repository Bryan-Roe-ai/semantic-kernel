"""Interactive Semantic Kernel demo for terminal chat sessions.

This sample shows how to wire up a :class:`~semantic_kernel.Kernel` with an
Ollama chat completion service and talk to it from an interactive terminal
session. It also exposes a small repository exploration plugin so the agent can
inspect local files when answering questions.
"""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path
from typing import Annotated

from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.ollama import OllamaChatCompletion
from semantic_kernel.functions import kernel_function


DEFAULT_INSTRUCTIONS = " ".join(
    [
        "You are a helpful assistant for the Semantic Kernel repository.",
        "Use the repo plugin to inspect files or directories before answering",
        "questions about the project.",
        "Include the file paths you reference in your responses.",
    ]
)


def parse_arguments() -> argparse.Namespace:
    """Parse CLI arguments for the interactive demo."""

    parser = argparse.ArgumentParser(
        description="Chat with Semantic Kernel through an interactive terminal."
    )
    parser.add_argument(
        "--model",
        default="llama2",
        help="Ollama model ID to use for chat completions (default: %(default)s)",
    )
    parser.add_argument(
        "--endpoint",
        default="http://localhost:11434",
        help="Base URL for the Ollama service (default: %(default)s)",
    )
    parser.add_argument(
        "--instructions",
        default=DEFAULT_INSTRUCTIONS,
        help="System prompt for the chat agent.",
    )
    parser.add_argument(
        "--disable-repo-plugin",
        action="store_true",
        help="Do not register the repository exploration plugin.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Root directory exposed by the repo plugin.",
    )
    parser.add_argument(
        "--initial-message",
        help="Send an initial message before starting the interactive loop.",
    )
    return parser.parse_args()

class RepoFilePlugin:
    """Expose simple read-only access to files in this repository."""

    def __init__(self, root: Path | None = None) -> None:
        self._root = (root or Path(__file__).resolve().parent).resolve()

    def _resolve_path(self, relative_path: str) -> Path:
        path = (self._root / relative_path).resolve()
        try:
            path.relative_to(self._root)
        except ValueError as error:  # pragma: no cover - defensive path check
            raise FileNotFoundError(
                f"Path '{relative_path}' is outside of the repository root."
            ) from error
        return path

    @kernel_function(description="Read the contents of a repository file.")
    def read_file(
        self, relative_path: Annotated[str, "A file path relative to the repository root."]
    ) -> Annotated[str, "Contents of the requested file."]:
        path = self._resolve_path(relative_path)
        if not path.is_file():
            raise FileNotFoundError(f"File '{relative_path}' was not found in the repository.")
        return path.read_text(encoding="utf-8")

    @kernel_function(description="List files and folders within the repository.")
    def list_directory(
        self, relative_path: Annotated[str, "A directory path relative to the repository root."] = "."
    ) -> Annotated[str, "Newline-delimited items contained within the directory."]:
        path = self._resolve_path(relative_path)
        if not path.is_dir():
            raise FileNotFoundError(
                f"Directory '{relative_path}' was not found in the repository."
            )
        return "\n".join(sorted(entry.name for entry in path.iterdir()))


async def read_console_line(prompt: str) -> str | None:
    """Read a line of input from the terminal in a non-blocking fashion."""

    try:
        return await asyncio.to_thread(input, prompt)
    except EOFError:
        return None


async def chat_loop(
    agent: ChatCompletionAgent,
    *,
    thread: ChatHistoryAgentThread | None = None,
    initial_message: str | None = None,
):
    """Interact with the agent until the user exits."""

    if initial_message:
        print(f"You: {initial_message}")
        response = await agent.get_response(messages=initial_message, thread=thread)
        print(f"{agent.name}: {response.message}\n")
        thread = response.thread

    while True:
        message = await read_console_line("You: ")
        if message is None:
            print()
            break

        message = message.strip()
        if not message:
            continue

        if message.lower() in {"exit", "quit"}:
            break

        response = await agent.get_response(messages=message, thread=thread)
        print(f"{agent.name}: {response.message}\n")
        thread = response.thread


async def main() -> None:
    args = parse_arguments()

    kernel = Kernel()
    service_id = "ollama-chat"
    kernel.add_service(
        OllamaChatCompletion(
            service_id=service_id,
            ai_model_id=args.model,
            host=args.endpoint,
        )
    )

    if not args.disable_repo_plugin:
        kernel.add_plugin(
            plugin=RepoFilePlugin(root=args.repo_root),
            plugin_name="repo",
        )

    agent = ChatCompletionAgent(
        kernel=kernel,
        name="RepoGuide",
        instructions=args.instructions,
        function_choice_behavior=FunctionChoiceBehavior.Auto(),
    )

    print("=" * 50)
    print("Semantic Kernel Demo - Interactive Chat")
    print("=" * 50)
    print(
        "Type your questions and press Enter to chat with the agent. "
        "Type 'exit' or press Ctrl+D to quit."
    )
    if not args.disable_repo_plugin:
        print(
            "The repo plugin is enabled, allowing the agent to browse files under "
            f"{args.repo_root}."
        )
    print()

    await chat_loop(agent, initial_message=args.initial_message)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")
