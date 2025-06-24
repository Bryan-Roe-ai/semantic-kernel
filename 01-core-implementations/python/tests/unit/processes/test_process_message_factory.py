#!/usr/bin/env python3
"""
Test module for process message factory

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from semantic_kernel.processes.kernel_process.kernel_process_edge import KernelProcessEdge
from semantic_kernel.processes.kernel_process.kernel_process_function_target import KernelProcessFunctionTarget
from semantic_kernel.processes.process_message_factory import ProcessMessageFactory


def test_create_from_edge():
    """Test initialization of KernelProcessEdge with valid input."""
    source_step_id = "step_1"
    output_target = KernelProcessFunctionTarget(
        step_id="step_2", function_name="process_data", parameter_name="input_data", target_event_id="event_1"
    )
    edge = KernelProcessEdge(source_step_id=source_step_id, output_target=output_target)

    process_message = ProcessMessageFactory.create_from_edge(edge, "data")

    assert process_message.source_id == source_step_id
