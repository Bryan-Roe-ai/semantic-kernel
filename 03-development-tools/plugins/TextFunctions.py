#!/usr/bin/env python3
"""
Textfunctions module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

from typing import List, Optional

from semantic_kernel.functions.kernel_function_decorator import kernel_function

class TextFunctions:
    """A collection of text processing functions."""

    @kernel_function(
        description="Analyze text and count occurrences of a specific word",
        name="count_word"
    )
    def count_word_occurrences(self, text: str, word: str) -> str:
        """
        Count occurrences of a specific word in the text.
        
        Args:
            text: The text to analyze
            word: The word to count
            
        Returns:
            The count as a string
        """
        if not text or not word:
            return "0"
            
        # Normalize to lowercase and split by spaces
        words = text.lower().split()
        word_to_find = word.lower()
        
        # Count occurrences
        count = words.count(word_to_find)
        return str(count)
        
    @kernel_function(
        description="Extract all email addresses from text",
        name="extract_emails"
    )
    def extract_emails(self, text: str) -> str:
        """
        Extract all email addresses from the input text.
        
        Args:
            text: The text to analyze
            
        Returns:
            Comma-separated list of email addresses
        """
        import re
        
        if not text:
            return "No emails found"
            
        # Regular expression for email matching
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        
        # Find all matches
        emails = re.findall(email_pattern, text)
        
        if emails:
            return ", ".join(emails)
        else:
            return "No emails found"
            
    @kernel_function(
        description="Format text as a bullet list",
        name="bullet_list"
    )
    def format_bullet_list(self, text: str, delimiter: Optional[str] = ",") -> str:
        """
        Format a delimited string as a bullet list.
        
        Args:
            text: The text to format
            delimiter: The delimiter to split by (default: comma)
            
        Returns:
            Formatted bullet list
        """
        if not text:
            return "Empty input"
            
        # Split the text by the delimiter
        items = [item.strip() for item in text.split(delimiter) if item.strip()]
        
        # Format as bullet list
        if items:
            return "\n".join([f"• {item}" for item in items])
        else:
            return "No items to format"
