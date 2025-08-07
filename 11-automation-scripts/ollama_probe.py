#!/usr/bin/env python3
"""
Ollama Probe module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import httpx

endpoints = [
    "http://localhost:11434/api/generate",
    "http://localhost:11434/api/chat",
    "http://localhost:11434/api/tags",
    "http://localhost:11434/",
]

for url in endpoints:
    try:
        print(f"Testing: {url}")
        resp = httpx.get(url, timeout=5)
        print(f"Status: {resp.status_code}")
        print(f"Body: {resp.text[:200]}\n")
    except Exception as e:
        print(f"Error: {e}\n")
