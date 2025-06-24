#!/usr/bin/env python3
"""
Datafunctions module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Data utilities plugin for LM Studio Chat
import json
import base64
from typing import Optional

from semantic_kernel.functions.kernel_function_decorator import kernel_function

class DataFunctions:
    """Functions to handle data transformations."""

    @kernel_function(
        description="Convert JSON to formatted, readable text",
        name="format_json"
    )
    def format_json(self, json_string: str) -> str:
        """
        Format JSON string to make it more readable.
        
        Args:
            json_string: The JSON string to format
            
        Returns:
            Formatted JSON string
        """
        try:
            # Parse the JSON
            data = json.loads(json_string)
            
            # Format with indentation
            formatted_json = json.dumps(data, indent=2, sort_keys=True)
            
            return formatted_json
        except Exception as e:
            return f"Error formatting JSON: {str(e)}"
    
    @kernel_function(
        description="Encode text to base64",
        name="encode_base64"
    )
    def encode_base64(self, text: str) -> str:
        """
        Encode text to base64.
        
        Args:
            text: The text to encode
            
        Returns:
            Base64 encoded string
        """
        try:
            # Convert to bytes and encode
            encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
            return encoded
        except Exception as e:
            return f"Error encoding to base64: {str(e)}"
    
    @kernel_function(
        description="Decode base64 to text",
        name="decode_base64"
    )
    def decode_base64(self, encoded: str) -> str:
        """
        Decode base64 to text.
        
        Args:
            encoded: The base64 encoded string
            
        Returns:
            Decoded text
        """
        try:
            # Decode from base64
            decoded = base64.b64decode(encoded).decode('utf-8')
            return decoded
        except Exception as e:
            return f"Error decoding from base64: {str(e)}"
    
    @kernel_function(
        description="Convert CSV to JSON format",
        name="csv_to_json"
    )
    def csv_to_json(self, csv_text: str) -> str:
        """
        Convert CSV text to JSON format.
        
        Args:
            csv_text: CSV data with header row
            
        Returns:
            JSON representation of the CSV data
        """
        import csv
        from io import StringIO
        
        try:
            # Parse CSV using a string buffer
            csv_buffer = StringIO(csv_text.strip())
            reader = csv.DictReader(csv_buffer)
            
            # Convert to list of dictionaries
            rows = list(reader)
            
            # Convert to JSON
            return json.dumps(rows, indent=2)
        except Exception as e:
            return f"Error converting CSV to JSON: {str(e)}"
