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
- File uploads and processing
- Data visualization capabilities
- Chat history persistence
- Visual plugin results

## Backend API

The `backend.py` serves as a bridge between the web interfaces and LM Studio's API:

- `/ping` - Check if the backend is running
- `/api/chat` - Send chat messages to LM Studio
- `/api/plugins` - List available plugins
- `/api/run_plugin` - Execute directory-based plugins
- `/api/run_python` - Execute Python-based plugins
- `/files/list` and `/files/read` - Basic file operations
- `/api/upload` - Upload files to the server
- `/api/files` - List all uploaded files
- `/api/download/{filename}` - Download uploaded files

## Plugins

Plugins are stored in the `plugins/` directory and come in two types:

### Directory-based Plugins

```
plugins/
├─ plugin-name/
│  ├─ function-name/
│  │  ├─ skprompt.txt  # Prompt template
│  │  ├─ config.json   # Configuration
```

### Python-based Plugins

```
plugins/
├─ PluginNameFunctions.py  # Python plugin class
```

Sample plugins are included:

#### Directory-based Plugins:

- `math/calculate` - Performs calculations
- `text/summarize` - Summarizes text

#### Python-based Plugins:

- `MathFunctions.py` - Advanced math operations
- `TextFunctions.py` - Text processing utilities
- `FileOperationsFunctions.py` - File system operations
- `DataAnalysisFunctions.py` - Data analysis and visualization
- `DataFunctions.py` - Data format conversion utilities

## Customization

- Edit HTML/CSS for visual customization
- Modify backend.py for API changes
- Create your own plugins in the plugins directory

## Troubleshooting

- **Connection errors**: Ensure both LM Studio API and backend servers are running
- **API errors**: Check that LM Studio has a model loaded and API enabled
- **Plugin errors**: Verify plugin directory structure and prompt templates
- **File upload issues**: Make sure the `uploads` directory exists and has write permissions
- **Python plugin errors**: Install required Python packages (matplotlib, numpy) for data analysis plugins
- **Chart generation failures**: Ensure matplotlib is installed for visualization features

## System Requirements

- Python 3.9 or higher
- LM Studio with API server enabled
- Web browser supporting modern JavaScript
- Optional: matplotlib and numpy for data visualization plugins

## New Features

### File Uploads

The interface now supports uploading files that can be processed by plugins:

- Upload files via the paperclip icon in the chat interface
- Reference uploaded files in your chat messages
- Process CSV and JSON files with data analysis plugins

### Data Analysis

New data analysis plugins offer advanced capabilities:

- `DataAnalysis.AnalyzeCsv` - Extract statistics and insights from CSV files
- `DataAnalysis.ParseJson` - Navigate and extract data from JSON structures
- `DataAnalysis.GenerateChart` - Create visualizations (bar, line, scatter, pie charts)

### Chat History

Chat conversations are now saved in your browser's local storage:

- Conversations persist between sessions
- Visual indicators for older conversations
- Clear chat button to start fresh

See `UPDATES.md` for more details on the latest features.
