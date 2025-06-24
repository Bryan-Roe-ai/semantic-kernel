#!/usr/bin/env python3
"""
Test module for default termination strategy

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.


from semantic_kernel.agents.strategies.termination.default_termination_strategy import DefaultTerminationStrategy


async def test_should_agent_terminate_():
    strategy = DefaultTerminationStrategy(maximum_iterations=2)
    result = await strategy.should_agent_terminate(None, [])
    assert not result
