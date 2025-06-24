#!/usr/bin/env python3
"""
Val Block module

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
from re import S, compile
from typing import TYPE_CHECKING, Any, ClassVar

from pydantic import model_validator

from semantic_kernel.exceptions import ValBlockSyntaxError
from semantic_kernel.template_engine.blocks.block import Block
from typing import TYPE_CHECKING, Any, ClassVar, Optional, Tuple

from pydantic import model_validator

from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.template_engine.blocks.block_errors import ValBlockSyntaxError
from typing import TYPE_CHECKING, Any, ClassVar, Optional, Tuple

from pydantic import model_validator

from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.template_engine.blocks.block_errors import ValBlockSyntaxError
from typing import TYPE_CHECKING, Any, ClassVar, Optional, Tuple

from pydantic import model_validator

from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.template_engine.blocks.block_errors import ValBlockSyntaxError
from semantic_kernel.template_engine.blocks.block_types import BlockTypes

if TYPE_CHECKING:
    from semantic_kernel.functions.kernel_arguments import KernelArguments
    from semantic_kernel.kernel import Kernel

logger: logging.Logger = logging.getLogger(__name__)

VAL_BLOCK_REGEX = r"^(?P<quote>[\"'])(?P<value>.*)(?P=quote)$"

VAL_BLOCK_MATCHER = compile(VAL_BLOCK_REGEX, flags=S)


class ValBlock(Block):
    """Create a value block.

    A value block is used to represent a value in a template.
    It can be used to represent any characters.
    It needs to start and end with the same quote character,
    can be both single or double quotes, as long as they are not mixed.

    Examples:
        'value'
        "value"
        'value with "quotes"'
        "value with 'quotes'"

    Args:
        content - str : The content of the value block.
        value - str: The value of the block.
        quote - str: The quote used to wrap the value.

    Raises:
        ValBlockSyntaxError: If the content does not match the value block syntax.

    """

    type: ClassVar[BlockTypes] = BlockTypes.VALUE
    value: str | None = ""
    quote: str | None = "'"
    value: str | None = ""
    quote: str | None = "'"
    value: str | None = ""
    quote: str | None = "'"
    value: Optional[str] = ""
    quote: Optional[str] = "'"

    @model_validator(mode="before")
    @classmethod
    def parse_content(cls, fields: Any) -> Any:
        """Parse the content and extract the value and quote.

        The parsing is based on a regex that returns the value and quote.
        if the 'value' is already present then the parsing is skipped.
        """
        if isinstance(fields, Block) or "value" in fields:
            return fields
        content = fields.get("content", "").strip()
        matches = VAL_BLOCK_MATCHER.match(content)
        if not matches:
            raise ValBlockSyntaxError(content=content)
        if value := matches.groupdict().get("value"):
            fields["value"] = value
        if quote := matches.groupdict().get("quote"):
            fields["quote"] = quote
        return fields

    def render(self, *_: "Kernel | KernelArguments | None") -> str:
        """Render the value block."""
        return self.value or ""
    def render(self, *_: "Kernel | KernelArguments | None") -> str:
        """Render the value block."""
        return self.value or ""
    def render(self, *_: "Kernel | KernelArguments | None") -> str:
        """Render the value block."""
        return self.value or ""
    def render(self, *_: Tuple["Kernel", Optional["KernelArguments"]]) -> str:
        return self.value
from logging import Logger
from typing import Optional, Tuple

from semantic_kernel.orchestration.context_variables import ContextVariables
from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.template_engine.blocks.block_types import BlockTypes
from semantic_kernel.template_engine.blocks.symbols import Symbols
from semantic_kernel.template_engine.protocols.text_renderer import TextRenderer


class ValBlock(Block, TextRenderer):
    def __init__(self, content: Optional[str] = None, log: Optional[Logger] = None):
        super().__init__(content=content and content.strip(), log=log)

        if len(self.content) < 2:
            err = "A value must have single quotes or double quotes on both sides"
            self.log.error(err)
            self._value = ""
            self._first = "\0"
            self._last = "\0"
            return

        self._first = self.content[0]
        self._last = self.content[-1]
        self._value = self.content[1:-1]

    @property
    def type(self) -> BlockTypes:
        return BlockTypes.VALUE

    def is_valid(self) -> Tuple[bool, str]:
        if len(self.content) < 2:
            error_msg = "A value must have single quotes or double quotes on both sides"
            self.log.error(error_msg)
            return False, error_msg

        if self._first != Symbols.DBL_QUOTE and self._first != Symbols.SGL_QUOTE:
            error_msg = (
                "A value must be wrapped in either single quotes or double quotes"
            )
            self.log.error(error_msg)
            return False, error_msg

        if self._first != self._last:
            error_msg = (
                "A value must be defined using either single quotes or "
                "double quotes, not both"
            )
            self.log.error(error_msg)
            return False, error_msg

        return True, ""

    def render(self, _: Optional[ContextVariables] = None) -> str:
        return self._value

    @staticmethod
    def has_val_prefix(text: Optional[str]) -> bool:
        return (
            text is not None
            and len(text) > 0
            and (text[0] == Symbols.DBL_QUOTE or text[0] == Symbols.SGL_QUOTE)
        )
