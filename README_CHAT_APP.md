# AI Chat Application

An easy-to-use local AI chat interface powered by LM Studio and FastAPI.

## Overview

This application provides a web-based chat interface to interact with AI models running in LM Studio. It features multiple user interfaces, file analysis capabilities, and a robust backend system.

## Features

- **Multiple Chat Interfaces**: Choose from simple, standard, or advanced interfaces
- **File Analysis**: Upload and analyze various file types (text, CSV, JSON, images)
- **Local AI Integration**: Connect with LM Studio's local AI models
- **Plugin System**: Extend functionality through a simple plugin architecture
- **Error Handling**: Robust error recovery and helpful diagnostic messages

## Getting Started

### Quick Start

1. Make sure [LM Studio](https://lmstudio.ai/) is installed and running
2. Start the LM Studio API server from the API tab
3. Run the unified start script:

```bash
python start_chat_unified.py
```

Or for Windows users, simply double-click:

```
start_ai_chat.bat
```

### First-Time Setup

If this is your first time running the application, you can use the setup script:

```bash
python setup.py
```

This script will:

- Check Python version compatibility
- Install all required dependencies
- Create necessary directories
- Generate default configuration files

For detailed setup instructions, see [SETUP_AND_USAGE.md](SETUP_AND_USAGE.md).

## Troubleshooting

If you're experiencing issues, use the test script to diagnose problems:

```bash
python test_backend.py
```

This script will check:

- If the backend server is running
- If LM Studio is accessible
- If the chat functionality is working correctly

## Available Scripts

- `start_chat_unified.py`: All-in-one script to start the chat application
- `setup.py`: First-time setup script
- `test_backend.py`: Diagnostic script to check system connectivity
- `start_ai_chat.bat`: Windows batch file launcher
- `backend.py`: The main backend server implementation

## Configuration

The application uses a `.env` file for configuration:

```
LM_STUDIO_URL="http://localhost:1234/v1/chat/completions"
```

You can modify this file to change the LM Studio URL if needed.

## File Analysis Capabilities

The application can analyze various file types:

- **Text files**: Line count, word count, preview
- **CSV files**: Headers, row count, sample data
- **JSON files**: Structure, key count, sample data
- **Images**: File format, dimensions (requires Pillow)
- **Documents**: Basic metadata for common document types

## System Requirements

- Python 3.8 or higher
- LM Studio
- Web browser supporting modern JavaScript features

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
