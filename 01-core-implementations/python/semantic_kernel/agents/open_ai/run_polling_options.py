#!/usr/bin/env python3
"""
Run Polling Options module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from datetime import timedelta

from pydantic import Field

from semantic_kernel.kernel_pydantic import KernelBaseModel
from semantic_kernel.utils.feature_stage_decorator import experimental

@experimental
class RunPollingOptions(KernelBaseModel):
    """Configuration and defaults associated with polling behavior for Assistant API requests."""

    default_polling_interval: timedelta = Field(default=timedelta(milliseconds=250))
    default_polling_backoff: timedelta = Field(default=timedelta(seconds=1))
    default_polling_backoff_threshold: int = Field(default=2)
    default_message_synchronization_delay: timedelta = Field(
        default=timedelta(milliseconds=250)
    )
    run_polling_interval: timedelta = Field(default=timedelta(milliseconds=250))
    run_polling_backoff: timedelta = Field(default=timedelta(seconds=1))
    run_polling_backoff_threshold: int = Field(default=2)
    message_synchronization_delay: timedelta = Field(
        default=timedelta(milliseconds=250)
    )
    message_synchronization_delay: timedelta = Field(
        default=timedelta(milliseconds=250)
    )
    message_synchronization_delay: timedelta = Field(default=timedelta(milliseconds=250))
    run_polling_timeout: timedelta = Field(default=timedelta(minutes=1))  # New timeout attribute

    def get_polling_interval(self, iteration_count: int) -> timedelta:
        """Get the polling interval for the given iteration count."""
        return (
            self.run_polling_backoff
            if iteration_count > self.run_polling_backoff_threshold
            else self.run_polling_interval
        )
