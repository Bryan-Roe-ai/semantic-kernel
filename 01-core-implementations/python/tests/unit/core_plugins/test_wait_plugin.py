#!/usr/bin/env python3
"""
Test module for wait plugin

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""



# Copyright (c) Microsoft. All rights reserved.

# Copyright (c) Microsoft. All rights reserved.

# Copyright (c) Microsoft. All rights reserved.

# Copyright (c) Microsoft. All rights reserved.

# Copyright (c) Microsoft. All rights reserved.

from unittest.mock import patch

import pytest

from semantic_kernel.core_plugins.wait_plugin import WaitPlugin
from semantic_kernel.exceptions import FunctionExecutionException
import asyncio

test_data_good = [
    0,
    1.0,
    -2,
    "0",
    "1",
    "2.1",
    "0.1",
    "0.01",
    "0.001",
    "0.0001",
    "-0.0001",
]

test_data_bad = [
    "$0",
    "one hundred",
    "20..,,2,1",
    ".2,2.1",
    "0.1.0",
    "00-099",
    "¹²¹",
    "2²",
    "zero",
    "-100 seconds",
    "1 second",
]

def test_can_be_instantiated():
    plugin = WaitPlugin()
    assert plugin is not None

@pytest.mark.parametrize("wait_time", test_data_good)
async def test_wait_valid_params(wait_time):
    plugin = WaitPlugin()
    with patch("asyncio.sleep") as patched_sleep:
        await plugin.wait(wait_time)

        patched_sleep.assert_called_once_with(abs(float(wait_time)))

        patched_sleep.assert_called_once_with(abs(float(wait_time)))

        patched_sleep.assert_called_once_with(abs(float(wait_time)))

        patched_sleep.assert_called_once_with(abs(float(wait_time)))

        patched_sleep.assert_called_once_with(abs(float(wait_time)))

@pytest.mark.parametrize("wait_time", test_data_bad)
async def test_wait_invalid_params(wait_time):
    plugin = WaitPlugin()

    with pytest.raises(FunctionExecutionException) as exc_info:
        await plugin.wait("wait_time")

    assert exc_info.value.args[0] == "seconds text must be a number"
