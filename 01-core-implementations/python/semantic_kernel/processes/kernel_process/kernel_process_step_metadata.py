#!/usr/bin/env python3
"""
Kernel Process Step Metadata module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from dataclasses import dataclass

from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
@dataclass(frozen=True)
class KernelProcessStepMetadataAttribute:
    """Metadata describing the version of the Step's implementation for serialization and replay."""

    version: str = "v1"


@experimental
def kernel_process_step_metadata(version: str = "v1"):
    """Decorator to attach a version string representing the Step's implementation version.

    This version is serialized in `versionInfo` for each step, enabling replay
    and process recovery to instantiate the correct Step variant.

    The version string used in @kernel_process_step_metadata must uniquely identify the Step class'
    behavior and contract version. Different versions imply incompatible step behavior, state schema,
    or function/event definitions.

    Example usage:
        @kernel_process_step_metadata("CutFoodStep.V2")
        class CutFoodWithSharpeningStep(KernelProcessStep[MyState]):
            ...
    """

    def decorator(cls):
        setattr(cls, "_kernel_process_step_metadata", KernelProcessStepMetadataAttribute(version))
        return cls

    return decorator
