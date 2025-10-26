# AI Chat App Demo

This demo provides a ready-to-run chat experience powered by Semantic Kernel's `ChatCompletionAgent`.
It highlights how to wire a kernel, register plugins, and expose a multi-turn chat loop that can
be used as a lightweight copilot for day planning and Q&A scenarios.

## Features

- **Multi-turn agent chat** powered by any chat completion service configured for Semantic Kernel.
- **Auto-invoked plugins** that expose the current time and a simple note pad the agent can use.
- **Built-in commands** (`/help`, `/reset`, `/notes`, `/exit`) to control the session while you chat.

## Prerequisites

1. Install the Python package dependencies for the repo (for example using `pip install -e .` from the
   `python/` folder).
2. Configure credentials for either Azure OpenAI or OpenAI. The demo uses
   [`samples/sk_service_configurator.py`](../../sk_service_configurator.py) which relies on the
   `ServiceSettings` class. The easiest approach is to create a `.env` file next to this README and
   set the variables described in [`samples/README.md`](../../README.md).

## Running the demo

From the repository root:

```bash
cd python
python -m samples.demos.ai_chat_app.chat_app
```

When the application starts you can type natural language prompts. The following helper commands are
always available:

| Command   | Description |
|-----------|-------------|
| `/help`   | Print a short description of the demo and available commands. |
| `/reset`  | Start a fresh chat session. |
| `/notes`  | Show anything the agent stored via the note taking plugin. |
| `/exit`   | Quit the application. |

## Expected output

Below is a shortened example session using the OpenAI GPT-4o model.

```
Welcome to Finch, your Semantic Kernel powered chat companion!
Type anything to start the conversation.
Use /help for a list of commands or /exit to quit.
You:> let's plan tomorrow morning
Finch:> Absolutely! Here's a focused plan for your morning tomorrow:
... (assistant response trimmed) ...
You:> remember that I need to water the plants at 7am
Finch:> Got it! I've saved a note to water the plants at 7 a.m. tomorrow.
You:> /notes
Notes plugin: You have 1 saved note:
1. Water the plants at 7am.
You:> thanks!
Finch:> You're very welcome! If there's anything else you'd like to plan or remember, just let me know.
```

Feel free to adapt the plugins or instructions to fit your own scenarios.
