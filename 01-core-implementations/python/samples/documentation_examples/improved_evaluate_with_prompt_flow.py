#!/usr/bin/env python3
"""
Improved Evaluate With Prompt Flow module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

from promptflow import PFClient

pf_client = PFClient()

inputs = {
    "text": "What would you have left if you spent $3 when you only had $2 to begin with"
}  # The inputs of the flow.
flow_result = pf_client.test(flow="perform_math", inputs=inputs)
print(f"Flow outputs: {flow_result}")
