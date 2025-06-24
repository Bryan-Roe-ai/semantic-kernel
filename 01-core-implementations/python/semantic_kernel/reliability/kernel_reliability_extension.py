#!/usr/bin/env python3
"""
Kernel Reliability Extension module

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
from abc import ABC

from pydantic import Field
from typing_extensions import deprecated

from semantic_kernel.kernel_pydantic import KernelBaseModel
from semantic_kernel.reliability.pass_through_without_retry import (
    PassThroughWithoutRetry,
)
from semantic_kernel.reliability.retry_mechanism_base import RetryMechanismBase

logger: logging.Logger = logging.getLogger(__name__)


class KernelReliabilityExtension(KernelBaseModel, ABC):
    """Kernel reliability extension."""

    retry_mechanism: RetryMechanismBase = Field(
        default_factory=PassThroughWithoutRetry,
        exclude=True,
        deprecated=deprecated("retry_mechanism is deprecated; This property doesn't have any effect on the kernel."),
    )
