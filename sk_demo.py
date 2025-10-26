"""
Simple Semantic Kernel Demo
This demonstrates basic SK capabilities with Ollama
"""

import asyncio
from pathlib import Path
from typing import Annotated

from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.ollama import OllamaChatCompletion
from semantic_kernel.functions import kernel_function

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


async def main():
    # Initialize the kernel and chat service
    kernel = Kernel()
    service_id = "ollama-chat"
    kernel.add_service(
        OllamaChatCompletion(
            service_id=service_id,
            ai_model_id="llama2",  # You can change this to your preferred model
            url="http://localhost:11434",
        )
    )

    # Register a simple repository exploration plugin
    kernel.add_plugin(plugin=RepoFilePlugin(), plugin_name="repo")

    # Create an agent so the model can automatically call the plugin when helpful
    agent = ChatCompletionAgent(
        kernel=kernel,
        name="RepoGuide",
        instructions=(
            "You are a helpful assistant for the Semantic Kernel repository. "
            "Use the repo plugin to inspect files or directories before answering "
            "questions about the project. Include the file paths you reference in your responses."
        ),
        function_choice_behavior=FunctionChoiceBehavior.Auto(),
    )

    print("=" * 50)
    print("Semantic Kernel Demo - Chat with Ollama")
    print("=" * 50)
    print()

    # Example conversation grounded in repository content
    user_messages = [
        "Hi RepoGuide! What's inside the root of this repository?",
        "Summarize the main goals described in README.md.",
        "Give me one example of where Python samples live in the repo.",
    ]

    thread: ChatHistoryAgentThread | None = None
    for user_msg in user_messages:
        print(f"User: {user_msg}")
        response = await agent.get_response(messages=user_msg, thread=thread)
        print(f"Assistant: {response.message}")
        print("-" * 50)
        print()
        thread = response.thread

if __name__ == "__main__":
    asyncio.run(main())
