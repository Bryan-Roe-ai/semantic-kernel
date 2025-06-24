#!/usr/bin/env python3
"""
System Step module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class SystemStep:
    thought: Optional[str] = None
    action: Optional[str] = None
    action_variables: Optional[Dict[str, str]] = field(default_factory=dict)
    observation: Optional[str] = None
    final_answer: Optional[str] = None
    original_response: Optional[str] = None
