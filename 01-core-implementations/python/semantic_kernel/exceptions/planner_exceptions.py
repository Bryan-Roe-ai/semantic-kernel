#!/usr/bin/env python3
"""
Planner Exceptions module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.


from semantic_kernel.exceptions.kernel_exceptions import KernelException


class PlannerException(KernelException):
    """Base class for all planner exceptions."""


class PlannerExecutionException(PlannerException):
    """Base class for all planner execution exceptions."""


class PlannerInvalidGoalError(PlannerException):
    """An error occurred while validating the goal."""


class PlannerInvalidPlanError(PlannerException):
    """An error occurred while validating the plan."""


class PlannerInvalidConfigurationError(PlannerException):
    """An error occurred while validating the configuration."""


class PlannerCreatePlanError(PlannerException):
    """An error occurred while creating the plan."""


__all__ = [
    "PlannerCreatePlanError",
    "PlannerException",
    "PlannerExecutionException",
    "PlannerInvalidConfigurationError",
    "PlannerInvalidGoalError",
    "PlannerInvalidPlanError",
]
