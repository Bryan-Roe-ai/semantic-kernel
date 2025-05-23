# LM Studio Chat Interface

A collection of HTML/JavaScript interfaces for interacting with AI models via LM Studio.

![LM Studio Chat](https://raw.githubusercontent.com/microsoft/semantic-kernel/main/docs/images/chat-sample.png)

## Quick Start

1. **Install LM Studio** - Download and install from [https://lmstudio.ai/](https://lmstudio.ai/)
2. **Start LM Studio**:
   - Open LM Studio
   - Load a model
   - Go to the "API" tab
   - Click "Start server" (defaults to port 1234)
3. **Run the backend server**:
   ```
   pip install fastapi uvicorn requests
   python -m uvicorn backend:app --reload
   ```
4. **Open the chat interface**:
   - Open `simple-chat.html` for basic chat
   - Open `ai-chat-launcher.html` for more options
   - Open `plugin-chat.html` to use plugins

**Alternatively, run the all-in-one launcher**:

```
.\start_chat.ps1   # PowerShell
start_chat.bat     # Windows Command Prompt
```

## Features

### Simple Chat (`simple-chat.html`)

- Basic chat interface
- Minimal UI with good UX
- Connection status indicators

### Advanced Chat (`ai-chat-launcher.html`)

- Model selection
- Temperature adjustment
- Max token control
- System prompt customization

### Plugin-Enabled Chat (`plugin-chat.html`)

- All advanced features plus:
- Plugin selection and usage
- Direct plugin invocation
- Visual plugin results

## Backend API

The `backend.py` serves as a bridge between the web interfaces and LM Studio's API:

- `/ping` - Check if the backend is running
- `/api/chat` - Send chat messages to LM Studio
- `/api/plugins` - List available plugins
- `/api/run_plugin` - Execute a specific plugin
- `/files/list` and `/files/read` - File operations

## Plugins

Plugins are stored in the `plugins/` directory with this structure:

```
plugins/
├─ plugin-name/
│  ├─ function-name/
│  │  ├─ skprompt.txt  # Prompt template
│  │  ├─ config.json   # Configuration
```

Sample plugins are included:

- `math/calculate` - Performs calculations
- `text/summarize` - Summarizes text

## Customization

- Edit HTML/CSS for visual customization
- Modify backend.py for API changes
- Create your own plugins in the plugins directory

## Troubleshooting

- **Connection errors**: Ensure both LM Studio API and backend servers are running
- **API errors**: Check that LM Studio has a model loaded and API enabled
- **Plugin errors**: Verify plugin directory structure and prompt templates

## System Requirements

- Python 3.9 or higher
- LM Studio with API server enabled
- Web browser supporting modern JavaScript
