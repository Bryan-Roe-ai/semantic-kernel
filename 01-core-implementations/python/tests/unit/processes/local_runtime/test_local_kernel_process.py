#!/usr/bin/env python3
"""
import asyncio
Test module for local kernel process

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from semantic_kernel.exceptions.process_exceptions import ProcessInvalidConfigurationException
from semantic_kernel.kernel import Kernel
from semantic_kernel.processes.kernel_process.kernel_process import KernelProcess
from semantic_kernel.processes.kernel_process.kernel_process_event import KernelProcessEvent
from semantic_kernel.processes.kernel_process.kernel_process_state import KernelProcessState
from semantic_kernel.processes.kernel_process.kernel_process_step_info import KernelProcessStepInfo
from semantic_kernel.processes.local_runtime.local_kernel_process import start
from semantic_kernel.processes.local_runtime.local_kernel_process_context import LocalKernelProcessContext


async def test_start_method():
    # Arrange
    state = MagicMock(spec=KernelProcessState)
    state.name = "startable_state"
    state.id = "test_id"
    steps = [MagicMock(spec=KernelProcessStepInfo)]
    process = KernelProcess(state=state, steps=steps)
    kernel = MagicMock(spec=Kernel)
    initial_event = MagicMock(spec=KernelProcessEvent)

    with (
        patch.object(LocalKernelProcessContext, "start_with_event", new=AsyncMock()) as mock_start_with_event,
        patch(
            "semantic_kernel.processes.local_runtime.local_kernel_process_context.LocalKernelProcessContext",
            autospec=True,
        ) as MockContext,
    ):
        mock_context_instance = MockContext.return_value
        mock_context_instance.__aenter__.return_value = mock_context_instance
        mock_context_instance.__aexit__ = AsyncMock()

        # Act
        result = await start(process=process, kernel=kernel, initial_event=initial_event)

        # Assert
        mock_start_with_event.assert_awaited_once_with(initial_event)
        assert isinstance(result, LocalKernelProcessContext)


async def test_failed_start():
    state = MagicMock(spec=KernelProcessState)
    state.name = "startable_state"
    state.id = "test_id"
    steps = [MagicMock(spec=KernelProcessStepInfo)]
    process = KernelProcess(state=state, steps=steps)
    kernel = MagicMock(spec=Kernel)
    initial_event = MagicMock(spec=KernelProcessEvent)

    with pytest.raises(ProcessInvalidConfigurationException):
        _ = await start(process=None, kernel=kernel, initial_event=initial_event)

    with pytest.raises(ProcessInvalidConfigurationException):
        _ = await start(process=process, kernel=None, initial_event=initial_event)

    with pytest.raises(ProcessInvalidConfigurationException):
        _ = await start(process=process, kernel=kernel, initial_event=None)
