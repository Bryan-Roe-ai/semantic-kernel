#!/usr/bin/env python3
"""
File Analyzer module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# File analysis module for LM Studio Chat
# This handles automatic file analysis based on file type

import os
import json
import csv
import mimetypes
from typing import Dict, Any

# Try to import optional dependencies without causing errors
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class FileAnalyzer:
    """Class for analyzing files of different types and providing insights."""

    @staticmethod
    def analyze_file(file_path: str) -> Dict[str, Any]:
        """
        Analyze a file based on its type and return structured insights

        Args:
            file_path: Path to the file

        Returns:
            Dictionary with analysis results
        """
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}

        # Get file extension and base name
        _, ext = os.path.splitext(file_path.lower())
        filename = os.path.basename(file_path)

        # Initialize analysis result
        analysis = {
            "type": "unknown",
            "summary": f"File: {filename}",
            "details": {}
        }

        # (unused binary check removed)

        # Analyze based on file extension
        try:
            if ext == '.csv':
                return FileAnalyzer._analyze_csv(file_path, analysis)
            elif ext == '.json':
                return FileAnalyzer._analyze_json(file_path, analysis)
            elif ext in ['.txt', '.md', '.log', '.py', '.js', '.html', '.css', '.xml']:
                return FileAnalyzer._analyze_text(file_path, analysis)
            elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff']:
                return FileAnalyzer._analyze_image(file_path, analysis)
            elif ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']:
                return FileAnalyzer._analyze_document(file_path, analysis)
            else:
                # Generic file info
                return FileAnalyzer._analyze_generic(file_path, analysis)
        except Exception as e:
            analysis["error"] = f"Analysis error: {str(e)}"
            return analysis

    @staticmethod
    def _is_binary_file(file_path: str, sample_size: int = 4096) -> bool:
        """
        Check if a file is binary by reading a sample and looking for null bytes

        Args:
            file_path: Path to the file
            sample_size: Number of bytes to sample for the check

        Returns:
            True if the file appears to be binary, False otherwise
        """
        try:
            with open(file_path, 'rb') as f:
                sample = f.read(sample_size)
                # Look for null bytes which usually indicate binary content
                return b'\x00' in sample
        except Exception:
            # If we can't read the file, assume it's binary to be safe
            return True

    @staticmethod
    def _analyze_csv(file_path: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze CSV files"""
        analysis["type"] = "csv"
        analysis["details"] = {}  # Initialize details dictionary

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    csv_reader = csv.reader(f)

                    # Try to get headers safely
                    try:
                        headers = next(csv_reader, [])
                    except csv.Error:
                        headers = []
                        analysis["details"]["warning"] = "Failed to parse CSV headers"

                    # Count rows (limited to first 1000 for performance)
                    row_count = 0
                    data_sample = []

                    for i, row in enumerate(csv_reader):
                        if i < 5:  # Get sample of first 5 rows
                            # Only create a sample entry if headers exist and row size matches headers
                            if headers and len(row) == len(headers):
                                try:
                                    data_sample.append(dict(zip(headers, row)))
                                except Exception:
                                    # If we can't create dict, just store the row
                                    data_sample.append({"row": row})
                        row_count += 1
                        if row_count >= 1000:
                            row_count = "1000+ (showing first 1000 only)"
                            break

                    analysis["details"] = {
                        "headers": headers,
                        "rowCount": row_count,
                        "sample": data_sample
                    }

                    analysis["summary"] = f"CSV file with {len(headers)} columns and {row_count} rows."
                except csv.Error as csv_error:
                    analysis["details"]["error"] = f"CSV parsing error: {str(csv_error)}"
                    analysis["summary"] = "CSV file (parsing error)"

        except UnicodeDecodeError:
            analysis["details"]["error"] = "CSV file contains non-UTF-8 characters"
            analysis["summary"] = "CSV file (encoding error)"
        except Exception as e:
            analysis["details"]["error"] = f"Error reading CSV: {str(e)}"
            analysis["summary"] = "CSV file (read error)"

        return analysis

    @staticmethod
    def _analyze_json(file_path: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze JSON files"""
        analysis["type"] = "json"

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    json_data = json.load(f)

                    # Determine if it's a dict or list
                    if isinstance(json_data, dict):
                        keys = list(json_data.keys())
                        analysis["details"] = {
                            "objectType": "object",
                            "keyCount": len(keys),
                            "topLevelKeys": keys[:10],  # First 10 keys
                            "hasMoreKeys": len(keys) > 10
                        }
                        analysis["summary"] = f"JSON object with {len(keys)} top-level keys."

                    elif isinstance(json_data, list):
                        analysis["details"] = {
                            "objectType": "array",
                            "length": len(json_data),
                            "sample": json_data[:3] if len(json_data) > 0 else []  # First 3 items
                        }
                        analysis["summary"] = f"JSON array with {len(json_data)} items."
                    else:
                        analysis["details"] = {
                            "objectType": "primitive",
                            "value": str(json_data)
                        }
                        analysis["summary"] = f"JSON primitive value: {str(json_data)[:50]}"
                except json.JSONDecodeError as e:
                    analysis["details"]["error"] = f"JSON syntax error: {str(e)}"
                    analysis["summary"] = "JSON file (invalid format)"
        except UnicodeDecodeError:
            analysis["details"]["error"] = "JSON file contains non-UTF-8 characters"
            analysis["summary"] = "JSON file (encoding error)"
        except Exception as e:
            analysis["details"]["error"] = f"Error reading JSON: {str(e)}"

        return analysis

    @staticmethod
    def _analyze_text(file_path: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze text files"""
        analysis["type"] = "text"

        try:
            # Try to detect if it's a binary file first
            if FileAnalyzer._is_binary_file(file_path):
                analysis["details"] = {"error": "File appears to be binary, not text"}
                analysis["summary"] = "Binary file detected (not text)"
                return analysis

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(10000)  # Read first 10000 chars

            lines = content.split('\n')
            line_count = len(lines)
            word_count = len(content.split())
            char_count = len(content)

            analysis["details"] = {
                "lineCount": line_count,
                "wordCount": word_count,
                "charCount": char_count,
                "preview": content[:300] + ('...' if len(content) > 300 else '')
            }

            analysis["summary"] = f"Text file with {line_count} lines and {word_count} words."

        except UnicodeDecodeError:
            # Try with latin-1 encoding as a fallback
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read(5000)

                lines = content.split('\n')
                line_count = len(lines)

                analysis["details"] = {
                    "lineCount": line_count,
                    "preview": content[:200] + ('...' if len(content) > 200 else ''),
                    "encoding": "latin-1 (non-UTF-8 characters detected)"
                }
                analysis["summary"] = f"Text file (non-UTF-8) with {line_count} lines."
            except Exception:
                analysis["details"] = {"error": "File encoding could not be determined"}
                analysis["summary"] = "Text file (encoding error)"
        except Exception as e:
            analysis["details"]["error"] = f"Error reading text file: {str(e)}"

        return analysis

    @staticmethod
    def _analyze_image(file_path: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze image files"""
        analysis["type"] = "image"

        try:
            mime_type, _ = mimetypes.guess_type(file_path)
            file_size = os.path.getsize(file_path)

            analysis["details"] = {
                "mimeType": mime_type or "image/unknown",
                "fileSize": file_size,
            }

            # If PIL is available, get image dimensions
            if PIL_AVAILABLE:
                try:
                    with Image.open(file_path) as img:
                        width, height = img.size
                        analysis["details"]["dimensions"] = f"{width} x {height}"
                        analysis["details"]["format"] = img.format
                        analysis["details"]["mode"] = img.mode
                except Exception as img_err:
                    analysis["details"]["pil_error"] = str(img_err)
            else:
                analysis["details"]["note"] = "Install Pillow for detailed image analysis"

            analysis["summary"] = f"Image file ({os.path.splitext(file_path)[1].replace('.', '')})"
            if "dimensions" in analysis["details"]:
                analysis["summary"] += f", {analysis['details']['dimensions']}"

        except Exception as e:
            analysis["details"]["error"] = f"Error analyzing image: {str(e)}"

        return analysis

    @staticmethod
    def _analyze_document(file_path: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Basic analysis for document files (PDF, Office documents, etc.)"""
        analysis["type"] = "document"

        try:
            mime_type, _ = mimetypes.guess_type(file_path)
            file_size = os.path.getsize(file_path)
            ext = os.path.splitext(file_path)[1].lower()

            # Format file size
            size_str = f"{file_size} bytes"
            if file_size > 1024:
                size_str = f"{file_size / 1024:.1f} KB"
            if file_size > 1024 * 1024:
                size_str = f"{file_size / (1024 * 1024):.1f} MB"

            analysis["details"] = {
                "fileType": ext.replace('.', '').upper(),
                "mimeType": mime_type or "application/unknown",
                "fileSize": file_size,
                "formattedSize": size_str,
                "note": "Document content extraction requires additional libraries"
            }

            doc_type_map = {
                '.pdf': 'PDF Document',
                '.doc': 'Word Document',
                '.docx': 'Word Document',
                '.xls': 'Excel Spreadsheet',
                '.xlsx': 'Excel Spreadsheet',
                '.ppt': 'PowerPoint Presentation',
                '.pptx': 'PowerPoint Presentation'
            }

            doc_type = doc_type_map.get(ext, 'Document')
            analysis["summary"] = f"{doc_type}, {size_str}"

        except Exception as e:
            analysis["details"]["error"] = f"Error analyzing document: {str(e)}"

        return analysis

    @staticmethod
    def _analyze_generic(file_path: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze any file type with basic information"""
        try:
            file_size = os.path.getsize(file_path)
            mime_type, _ = mimetypes.guess_type(file_path)
            is_binary = FileAnalyzer._is_binary_file(file_path)

            analysis["details"] = {
                "fileSize": file_size,
                "mimeType": mime_type or "unknown",
                "isBinary": is_binary
            }

            # Format file size
            size_str = f"{file_size} bytes"
            if file_size > 1024:
                size_str = f"{file_size / 1024:.1f} KB"
            if file_size > 1024 * 1024:
                size_str = f"{file_size / (1024 * 1024):.1f} MB"

            file_type = "Binary file" if is_binary else "Text file"
            analysis["summary"] = f"{file_type}: {os.path.basename(file_path)}, {size_str}"

        except Exception as e:
            analysis["details"]["error"] = f"Error analyzing file: {str(e)}"

        return analysis

# Main function for testing
if __name__ == "__main__":
    print("File Analyzer Module")
    # Test with a sample file if needed
    # test_file = "example.csv"
    # print(FileAnalyzer.analyze_file(test_file))
