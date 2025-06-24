#!/usr/bin/env python3
"""
Test module for logging

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

import logging

from semantic_kernel.utils.logging import setup_logging


def test_setup_logging():
    """Test that the logging is setup correctly."""
    setup_logging()

    root_logger = logging.getLogger()
    assert root_logger.handlers
    assert any(
        isinstance(handler, logging.StreamHandler) for handler in root_logger.handlers
    )
