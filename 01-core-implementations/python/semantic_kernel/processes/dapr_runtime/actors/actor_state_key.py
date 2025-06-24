#!/usr/bin/env python3
"""
Actor State Key module

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

from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
class ActorStateKeys(Enum):
    """Keys used to store actor state in Dapr."""

    # StepActor Keys
    StepParentProcessId = "parentProcessId"
    StepInfoState = "DaprStepInfo"
    StepStateJson = "kernelStepStateJson"
    StepStateType = "kernelStepStateType"
    StepIncomingMessagesState = "incomingMessagesState"

    # ProcessActor Keys
    ProcessInfoState = "DaprProcessInfo"
    StepActivatedState = "kernelStepActivated"

    # MessageBufferActor Keys
    MessageQueueState = "DaprMessageBufferState"

    # ExternalEventBufferActor Keys
    ExternalEventQueueState = "DaprExternalEventBufferState"

    # EventBufferActor Keys
    EventQueueState = "DaprEventBufferState"
