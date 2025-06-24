#!/usr/bin/env python3
"""
Test module for kernel process step state

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

import pytest
from pydantic import ValidationError

from semantic_kernel.processes.kernel_process.kernel_process_step_state import KernelProcessStepState


def test_initialization_with_name_and_id():
    # Arrange
    name = "step_state"
    step_id = "5678"

    # Act
    step_state = KernelProcessStepState(name=name, id=step_id, version="1.0")

    # Assert
    assert step_state.name == name
    assert step_state.id == step_id
    assert step_state.state is None


def test_initialization_with_name_only():
    # Arrange
    name = "step_state_without_id"

    # Act
    step_state = KernelProcessStepState(name=name, version="1.0")

    # Assert
    assert step_state.name == name
    assert step_state.id is None
    assert step_state.state is None


def test_setting_step_state_value():
    # Arrange
    name = "step_state"
    state_value = {"status": "in_progress"}

    # Act
    step_state = KernelProcessStepState(name=name, version="1.0")
    step_state.state = state_value

    # Assert
    assert step_state.state == state_value


def test_initialization_with_invalid_name():
    # Arrange
    name = 12345  # Invalid type for name

    # Act & Assert
    with pytest.raises(ValidationError):
        KernelProcessStepState(name=name)
