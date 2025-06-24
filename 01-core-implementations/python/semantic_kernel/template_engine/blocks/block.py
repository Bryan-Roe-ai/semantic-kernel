#!/usr/bin/env python3
"""
Block module

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
from typing import ClassVar

from pydantic import field_validator

from semantic_kernel.kernel_pydantic import KernelBaseModel
from semantic_kernel.template_engine.blocks.block_types import BlockTypes

logger: logging.Logger = logging.getLogger(__name__)


class Block(KernelBaseModel):
    """A block."""

    type: ClassVar[BlockTypes] = BlockTypes.UNDEFINED
    content: str

    @field_validator("content", mode="before")
    @classmethod
    def content_strip(cls, content: str):
        """Strip the content of the block."""
        return content.strip()
from abc import ABC, abstractmethod
from logging import Logger
from typing import Optional, Tuple

from semantic_kernel.orchestration.context_variables import ContextVariables
from semantic_kernel.orchestration.sk_context import SKContext
from semantic_kernel.template_engine.blocks.block_types import BlockTypes


class Block(ABC):
    _type: BlockTypes
    _content: str
    _log: Logger

    def __init__(self, block_type: BlockTypes, content: str, log: Logger) -> None:
        self._type = block_type
        self._content = content
        self._log = log

    async def render_code_async(self, context: SKContext) -> str:
        raise NotImplementedError("This block does not support code execution")

    @abstractmethod
    def is_valid(self) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def render(self, variables: Optional[ContextVariables]) -> str:
        pass
from logging import Logger
from typing import Optional, Tuple

from semantic_kernel.template_engine.blocks.block_types import BlockTypes
from semantic_kernel.utils.null_logger import NullLogger


class Block:
    def __init__(
        self, content: Optional[str] = None, log: Optional[Logger] = NullLogger
    ) -> None:
        self._content = content or ""
        self._log = log or NullLogger()
        self._type = BlockTypes.UNDEFINED

    @property
    def type(self) -> BlockTypes:
        return self._type

    @property
    def content(self) -> str:
        return self._content
    type: ClassVar[BlockTypes] = BlockTypes.UNDEFINED
    content: str

    @field_validator("content", mode="before")
    @classmethod
    def content_strip(cls, content: str):
        return content.strip()

    @property
    def log(self) -> Logger:
        return self._log

    def is_valid(self) -> Tuple[bool, str]:
        raise NotImplementedError("Subclasses must implement this method.")
