# Copyright (c) Microsoft. All rights reserved.

import asyncio
from textwrap import dedent
from typing import Annotated

from samples.sk_service_configurator import add_service
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.core_plugins import TimePlugin
from semantic_kernel.functions import KernelArguments, kernel_function

"""
This sample turns Semantic Kernel's ChatCompletionAgent into an interactive
command-line chat experience. The app relies on the following building blocks:
- a **ChatCompletionAgent** to reason over the conversation and invoke tools.
- a **ChatHistoryAgentThread** that keeps the conversation state between turns.
- a mix of **plugins** (the built-in `TimePlugin` plus a custom `NotesPlugin`) that
  can be auto-invoked by the agent when the user asks for time-sensitive help or
  requests to remember information.

The agent is called "Finch" and is configured to remember short notes using an
in-memory plugin. Tell Finch to "remember" something and you can retrieve it later
with the `/notes` command.
"""


class NotesPlugin:
    """A simple in-memory note taking plugin."""

    def __init__(self) -> None:
        self._notes: list[str] = []

    @kernel_function(description="Remember a short note for the user to recall later.")
    def remember_note(
        self,
        note: Annotated[str, "The note to store for the user."],
    ) -> Annotated[str, "Confirmation message after the note is stored."]:
        cleaned_note = note.strip()
        if not cleaned_note:
            return "I did not receive any text to remember."
        self._notes.append(cleaned_note)
        return "I've saved that in your notes."

    @kernel_function(description="Return all of the notes that are currently stored.")
    def list_notes(self) -> Annotated[str, "All notes stored in the notepad."]:
        if not self._notes:
            return "You have not asked me to remember anything yet."
        lines = ["Here is everything you asked me to remember:"]
        for index, value in enumerate(self._notes, start=1):
            lines.append(f"{index}. {value}")
        return "\n".join(lines)

    @kernel_function(description="Clear all stored notes when the user asks you to forget them.")
    def clear_notes(self) -> Annotated[str, "Confirmation that the notes were cleared."]:
        if not self._notes:
            return "There were no notes to forget."
        self._notes.clear()
        return "All saved notes are cleared."

    # Helper used by the CLI to display the state without calling into the agent.
    def render_notes(self) -> str:
        if not self._notes:
            return "Notes plugin: You do not have any saved notes yet."
        count = len(self._notes)
        plural = "s" if count != 1 else ""
        lines = [f"Notes plugin: You have {count} saved note{plural}:"]
        for index, value in enumerate(self._notes, start=1):
            lines.append(f"{index}. {value}")
        return "\n".join(lines)

    def reset(self) -> None:
        self._notes.clear()


HELP_TEXT = dedent(
    """
    Finch can help you plan your day, answer questions, and keep small notes.
    Commands:
      /help  - Show this message.
      /reset - Start a new conversation and forget stored notes.
      /notes - Display the notes saved by the plugin.
      /exit  - Quit the chat.
    """
).strip()

WELCOME_MESSAGE = dedent(
    """
    Welcome to Finch, your Semantic Kernel powered chat companion!
    Type anything to start the conversation.
    Use /help for a list of commands or /exit to quit.
    """
).strip()


async def main() -> None:
    # 1. Build the kernel and register AI + plugins.
    kernel = add_service(Kernel())
    notes_plugin = NotesPlugin()
    kernel.add_plugin(TimePlugin(), plugin_name="time")
    kernel.add_plugin(notes_plugin, plugin_name="notes")

    # 2. Configure function calling so the agent can call the plugins automatically.
    settings = kernel.get_prompt_execution_settings_from_service_id("default")
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
    settings.max_tokens = 800

    # 3. Create the chat completion agent with friendly instructions.
    agent = ChatCompletionAgent(
        kernel=kernel,
        name="Finch",
        description="A friendly AI sidekick that answers questions and keeps notes.",
        instructions=dedent(
            """
            You are Finch, a personable AI assistant.
            - Provide thoughtful but concise responses.
            - Use the `time` plugin when the user asks about the date or current time.
            - Use the `notes` plugin whenever the user asks you to remember, list, or clear notes.
            - When you store a note, confirm what you saved so the user can verify it.
            """
        ).strip(),
        arguments=KernelArguments(settings=settings),
    )

    thread: ChatHistoryAgentThread | None = None
    print(WELCOME_MESSAGE)

    while True:
        try:
            user_input = input("You:> ")
        except (KeyboardInterrupt, EOFError):
            print("\n\nExiting chat...")
            break

        normalized = user_input.strip()
        if not normalized:
            continue

        command = normalized.lower()
        if command in {"/exit", "exit", "quit"}:
            print("\n\nExiting chat...")
            break
        if command in {"/help", "help"}:
            print(HELP_TEXT)
            continue
        if command in {"/notes", "notes"}:
            print(notes_plugin.render_notes())
            continue
        if command in {"/reset", "reset"}:
            await thread.delete() if thread else None
            thread = None
            notes_plugin.reset()
            print("Started a new conversation and cleared stored notes.")
            continue

        response = await agent.get_response(messages=user_input, thread=thread)
        if response:
            speaker = response.name or agent.name or "Assistant"
            print(f"{speaker}:> {response}")
            thread = response.thread or thread
        else:
            print("Assistant:> I'm not sure how to respond to that just yet.")

    await thread.delete() if thread else None

    """
    Sample output:
    You:> remind me to send the status email at 5pm
    Finch:> I've saved a note to send the status email at 5 p.m. today. I'll be here if you need a reminder later!
    You:> /notes
    Notes plugin: You have 1 saved note:
    1. Send the status email at 5pm
    """


if __name__ == "__main__":
    asyncio.run(main())
