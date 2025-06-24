#!/usr/bin/env python3
"""
Fileoperations module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import base64
import os
import mimetypes
from typing import Optional

from semantic_kernel.functions.kernel_function_decorator import kernel_function

class FileOperationsFunctions:
    """Functions for handling file operations like uploads and downloads."""

    # The base directory for storing uploaded files
    UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")

    def __init__(self):
        """Initialize the file operations functions."""
        # Create uploads directory if it doesn't exist
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)

    @kernel_function(
        description="Save a base64 encoded file to the server",
        name="save_file"
    )
    def save_uploaded_file(self, base64_content: str, filename: str) -> str:
        """
        Save a base64 encoded file to the server.
        
        Args:
            base64_content: The base64 encoded content of the file
            filename: The name to give the file
            
        Returns:
            Path to the saved file or error message
        """
        if not base64_content or not filename:
            return "Error: Missing file content or filename"
            
        try:
            # Try to decode the base64 content
            file_content = base64.b64decode(base64_content)
            
            # Create a safe filename
            safe_filename = os.path.basename(filename)
            file_path = os.path.join(self.UPLOAD_DIR, safe_filename)
            
            # Write the file
            with open(file_path, "wb") as f:
                f.write(file_content)
                
            return f"File saved successfully: {safe_filename}"
        except Exception as e:
            return f"Error saving file: {str(e)}"

    @kernel_function(
        description="List all uploaded files",
        name="list_files"
    )
    def list_uploaded_files(self, filter_pattern: Optional[str] = None) -> str:
        """
        List all uploaded files, optionally filtered by a pattern.
        
        Args:
            filter_pattern: Optional pattern to filter files (e.g., "*.txt")
            
        Returns:
            A list of filenames
        """
        try:
            import glob
            
            # Get list of files
            if filter_pattern:
                files = glob.glob(os.path.join(self.UPLOAD_DIR, filter_pattern))
            else:
                files = [os.path.join(self.UPLOAD_DIR, f) for f in os.listdir(self.UPLOAD_DIR) 
                         if os.path.isfile(os.path.join(self.UPLOAD_DIR, f))]
            
            # Format the list
            if files:
                file_list = ["Available files:"]
                for file_path in files:
                    filename = os.path.basename(file_path)
                    size = os.path.getsize(file_path)
                    file_list.append(f"- {filename} ({self._format_size(size)})")
                return "\n".join(file_list)
            else:
                return "No files found"
        except Exception as e:
            return f"Error listing files: {str(e)}"
            
    @kernel_function(
        description="Read the contents of a file",
        name="read_file"
    )
    def read_file_content(self, filename: str) -> str:
        """
        Read the contents of an uploaded file.
        
        Args:
            filename: The name of the file to read
            
        Returns:
            The file contents or error message
        """
        try:
            # Create a safe filename
            safe_filename = os.path.basename(filename)
            file_path = os.path.join(self.UPLOAD_DIR, safe_filename)
            
            # Check if file exists
            if not os.path.exists(file_path):
                return f"Error: File {safe_filename} not found"
                
            # Read file content based on whether it's text or binary
            mimetype, _ = mimetypes.guess_type(file_path)
            
            if mimetype and mimetype.startswith('text/') or file_path.endswith(('.txt', '.md', '.csv', '.json')):
                # Text file
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                return f"File content of {safe_filename}:\n\n{content}"
            else:
                # Binary file - just return info
                size = os.path.getsize(file_path)
                return f"Binary file: {safe_filename} ({self._format_size(size)}). Use download_file to retrieve it."
        except Exception as e:
            return f"Error reading file: {str(e)}"
            
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in a human-readable format."""
        if size_bytes < 1024:
            return f"{size_bytes} bytes"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
