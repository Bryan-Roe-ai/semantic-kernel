# AI Chat Application Setup and Usage Guide

This document provides instructions for setting up and using the AI Chat application with LM Studio.

## Prerequisites

- Python 3.8 or higher
- LM Studio installed and configured
- A compatible web browser (Chrome, Firefox, Edge recommended)

## Quick Start

The easiest way to get started is to run the unified launcher script:

```bash
python start_chat_unified.py
```

This script will:

1. Check for and install required dependencies
2. Ensure the backend files exist
3. Create a default configuration if needed
4. Verify port availability
5. Check if LM Studio is running
6. Start the backend server
7. Open your chosen chat interface in your browser

## Manual Setup

If you prefer to set things up manually:

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file with the following content:

```
LM_STUDIO_URL="http://localhost:1234/v1/chat/completions"
```

Change the URL if your LM Studio is running on a different port or host.

### 3. Start LM Studio

1. Open LM Studio application
2. Go to the "API" tab
3. Click "Start server"
4. Make sure the server is running on port 1234 (or update your `.env` file accordingly)

### 4. Start the Backend Server

```bash
python -m uvicorn backend:app --reload --host 127.0.0.1 --port 8000
```

### 5. Open a Chat Interface

Open one of the following files in your web browser:

- advanced-ai-chat.html (Recommended)
- simple-chat.html
- ai-chat.html

## Available Chat Interfaces

- **Advanced Chat Interface**: Full-featured interface with file upload, system prompts, and more
- **Simple Chat Interface**: Minimalist interface focused just on chat
- **Standard Chat Interface**: Balanced interface with core features

## File Analysis Features

This application can analyze various file types:

- **Text files**: Count lines, words, and provide a preview
- **CSV files**: Show headers, row count, and sample data
- **JSON files**: Show structure and sample data
- **Images**: Show dimensions and format (requires Pillow library)
- **Documents**: Basic metadata for PDFs and Office documents

## Troubleshooting

### Backend won't start

- Check if port 8000 is already in use (the unified script will try to use a different port)
- Verify all dependencies are installed

### Can't connect to LM Studio

- Make sure LM Studio is running with the API server started
- Check the URL in your `.env` file matches the LM Studio API address
- Try accessing the LM Studio API directly with a tool like curl or Postman

### File uploads not working

- Check if you have write permissions to the "uploads" directory
- Some file types may not be supported for analysis

## Additional Resources

- See README.md for general project information
- See PLUGINS.md for information about extending the chat's capabilities
- Check the "docs" directory for detailed documentation on specific features

## Support

If you encounter any issues not covered in this guide, please open an issue in the project repository.
