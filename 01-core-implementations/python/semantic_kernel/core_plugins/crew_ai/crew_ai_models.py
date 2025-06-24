#!/usr/bin/env python3
"""
AI module for crew ai models

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from enum import Enum
from typing import Any

from semantic_kernel.kernel_pydantic import KernelBaseModel


class CrewAIEnterpriseKickoffState(str, Enum):
    """The Crew.AI Enterprise kickoff state."""

    Pending = "PENDING"
    Started = "STARTED"
    Running = "RUNNING"
    Success = "SUCCESS"
    Failed = "FAILED"
    Failure = "FAILURE"
    Not_Found = "NOT FOUND"


class CrewAIStatusResponse(KernelBaseModel):
    """Represents the status response from Crew AI."""

    state: CrewAIEnterpriseKickoffState
    result: str | None = None
    last_step: dict[str, Any] | None = None


class CrewAIKickoffResponse(KernelBaseModel):
    """Represents the kickoff response from Crew AI."""

    kickoff_id: str


class CrewAIRequiredInputs(KernelBaseModel):
    """Represents the required inputs for Crew AI."""

    inputs: dict[str, str]
