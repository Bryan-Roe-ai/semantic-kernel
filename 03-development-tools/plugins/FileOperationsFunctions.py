#!/usr/bin/env python3
"""
Fileoperationsfunctions module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# File operations plugin for LM Studio Chat
from typing import Optional
import os

from semantic_kernel.functions.kernel_function_decorator import kernel_function

class FileOperationsFunctions:
    """A collection of file operation functions."""

    @kernel_function(
        description="List files in a directory",
        name="list"
    )
    def list_files(self, path: str = "") -> str:
        """
        List files in the specified directory.

        Args:
            path: The directory path (relative to workspace root)

        Returns:
            List of files as a string
        """
        try:
            # Get workspace root
            workspace_dir = os.environ.get("WORKSPACE_DIR", os.getcwd())

            # Combine with the provided path
            target_dir = os.path.join(workspace_dir, path) if path else workspace_dir

            # List files
            if not os.path.exists(target_dir):
                return f"Directory not found: {path}"

            if not os.path.isdir(target_dir):
                return f"Not a directory: {path}"

            # Get files and directories
            items = os.listdir(target_dir)

            # Format output
            file_list = []
            for item in items:
                item_path = os.path.join(target_dir, item)
                item_type = "📁 " if os.path.isdir(item_path) else "📄 "
                file_list.append(f"{item_type}{item}")

            if not file_list:
                return "Directory is empty"

            return "\n".join(file_list)

        except Exception as e:
            return f"Error listing files: {str(e)}"

    @kernel_function(
        description="Read the contents of a file",
        name="read"
    )
    def read_file(self, file_path: str) -> str:
        """
        Read the contents of the specified file.

        Args:
            file_path: Path to the file (relative to workspace root)

        Returns:
            File contents as a string
        """
        try:
            # Get workspace root
            workspace_dir = os.environ.get("WORKSPACE_DIR", os.getcwd())

            # Combine with the provided path
            abs_path = os.path.abspath(os.path.join(workspace_dir, file_path))

            # Security check (prevent directory traversal)
            if not abs_path.startswith(workspace_dir):
                return f"Access denied: {file_path}"

            # Check if file exists
            if not os.path.exists(abs_path):
                return f"File not found: {file_path}"

            if not os.path.isfile(abs_path):
                return f"Not a file: {file_path}"

            # Read file
            with open(abs_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Limit content length if too large
            max_len = 4000
            if len(content) > max_len:
                content = content[:max_len] + f"\n\n... [truncated, {len(content) - max_len} characters remaining]"

            return content

        except Exception as e:
            return f"Error reading file: {str(e)}"

    @kernel_function(
        description="Get file information",
        name="info"
    )
    def file_info(self, file_path: str) -> str:
        """
        Get information about a file or directory.

        Args:
            file_path: Path to the file (relative to workspace root)

        Returns:
            File information as a string
        """
        try:
            # Get workspace root
            workspace_dir = os.environ.get("WORKSPACE_DIR", os.getcwd())

            # Combine with the provided path
            abs_path = os.path.abspath(os.path.join(workspace_dir, file_path))

            # Security check (prevent directory traversal)
            if not abs_path.startswith(workspace_dir):
                return f"Access denied: {file_path}"

            # Check if path exists
            if not os.path.exists(abs_path):
                return f"Path not found: {file_path}"

            # Get file/dir information
            info = []
            info.append(f"Name: {os.path.basename(abs_path)}")
            info.append(f"Type: {'Directory' if os.path.isdir(abs_path) else 'File'}")

            if os.path.isfile(abs_path):
                # File-specific info
                size_bytes = os.path.getsize(abs_path)
                size_display = f"{size_bytes} bytes"
                if size_bytes > 1024:
                    size_display += f" ({size_bytes / 1024:.2f} KB)"
                if size_bytes > 1024 * 1024:
                    size_display += f" ({size_bytes / (1024 * 1024):.2f} MB)"

                info.append(f"Size: {size_display}")

                # Get extension and determine type
                _, ext = os.path.splitext(abs_path)
                if ext:
                    info.append(f"Extension: {ext}")

            else:
                # Directory-specific info
                items = os.listdir(abs_path)
                info.append(f"Items: {len(items)}")
                info.append(f"Files: {sum(1 for item in items if os.path.isfile(os.path.join(abs_path, item)))}")
                info.append(f"Directories: {sum(1 for item in items if os.path.isdir(os.path.join(abs_path, item)))}")

            # Last modified time
            info.append(f"Last modified: {os.path.getmtime(abs_path)}")

            return "\n".join(info)

        except Exception as e:
            return f"Error getting file info: {str(e)}"
