#!/usr/bin/env python3
"""
Test module for kernel process state

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

from semantic_kernel.processes.kernel_process.kernel_process_state import KernelProcessState


def test_initialization_with_name_and_id():
    # Arrange
    name = "test_process"
    process_id = "1234"
    version = "1.0"

    # Act
    state = KernelProcessState(name=name, version=version, id=process_id)

    # Assert
    assert state.name == name
    assert state.id == process_id
    assert state.state is None
    assert state.version == version


def test_initialization_with_name_only():
    # Arrange
    name = "test_process_without_id"
    version = "1.0"

    # Act
    state = KernelProcessState(name=name, version=version)

    # Assert
    assert state.name == name
    assert state.id is None
    assert state.state is None
    assert state.version == version


def test_setting_state_value():
    # Arrange
    name = "test_process"
    state_value = {"key": "value"}

    # Act
    state = KernelProcessState(name=name, version="1.0")
    state.state = state_value

    # Assert
    assert state.state == state_value
    assert state.version == "1.0"


def test_initialization_with_invalid_name():
    # Arrange
    name = 12345  # Invalid type for name

    # Act & Assert
    with pytest.raises(ValidationError):
        KernelProcessState(name=name, version="1.0")
