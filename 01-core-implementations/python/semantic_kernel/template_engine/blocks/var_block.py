#!/usr/bin/env python3
"""
Var Block module

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
from re import compile
from typing import TYPE_CHECKING, Any, ClassVar, Optional

from pydantic import model_validator

from semantic_kernel.exceptions import VarBlockRenderError, VarBlockSyntaxError
from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.exceptions import VarBlockRenderError, VarBlockSyntaxError
from semantic_kernel.exceptions import VarBlockRenderError, VarBlockSyntaxError
from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.template_engine.blocks.block_errors import VarBlockSyntaxError
from semantic_kernel.exceptions import VarBlockRenderError, VarBlockSyntaxError
from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.template_engine.blocks.block_errors import VarBlockSyntaxError
from semantic_kernel.template_engine.blocks.block_types import BlockTypes
from semantic_kernel.template_engine.blocks.symbols import Symbols

if TYPE_CHECKING:
    from semantic_kernel.functions.kernel_arguments import KernelArguments
    from semantic_kernel.kernel import Kernel

logger: logging.Logger = logging.getLogger(__name__)

VAR_BLOCK_REGEX = r"^[${1}](?P<name>[0-9A-Za-z_]+)$"

VAR_BLOCK_MATCHER = compile(VAR_BLOCK_REGEX)


class VarBlock(Block):
    """Create a variable block.

    A variable block is used to add a variable to a template.
    It gets rendered from KernelArguments, if the variable is not found
    a warning is logged and an empty string is returned.
    The variable must start with $ and be followed by a valid variable name.
    A valid variable name is a string of letters, numbers and underscores.

    Examples:
        $var
        $test_var

    Args:
        content - str : The content of the variable block, the name of the variable.
        name - str: The name of the variable.

    Raises:
        VarBlockSyntaxError: If the content does not match the variable syntax.

    """

    type: ClassVar[BlockTypes] = BlockTypes.VARIABLE
    name: str = ""

    @model_validator(mode="before")
    @classmethod
    def parse_content(cls, fields: Any) -> Any:
        """Parse the content and extract the name.

        The parsing is based on a regex that returns the name.
        if the 'name' is already present then the parsing is skipped.
        """
        if isinstance(fields, Block) or "name" in fields:
            return fields
        content = fields.get("content", "").strip()
        matches = VAR_BLOCK_MATCHER.match(content)
        if not matches:
            raise VarBlockSyntaxError(content=content)
        if name := matches.groupdict().get("name"):
            fields["name"] = name
        return fields

    def render(self, _: "Kernel", arguments: Optional["KernelArguments"] = None) -> str:
        """Render the variable block with the given arguments.

        If the variable is not found in the arguments, return an empty string.
        """
        if arguments is None:
            return ""
        value = arguments.get(self.name, None)
        if value is None:
            logger.warning(
                f"Variable `{Symbols.VAR_PREFIX}: {self.name}` not found in the KernelArguments"
            )
            return ""
        try:
            return str(value)
        except Exception as e:
            raise VarBlockRenderError(
                f"Block {self.name} failed to be parsed to a string, type is {type(value)}"
            ) from e
from logging import Logger
from re import match as regex_match
from typing import Literal, Optional, Tuple
from logging import Logger
from re import match as re_match
from typing import Optional, Tuple

from semantic_kernel.orchestration.context_variables import ContextVariables
from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.template_engine.blocks.block_types import BlockTypes
from semantic_kernel.template_engine.template_exception import TemplateException
from semantic_kernel.utils.static_property import static_property


class VarBlock(Block):
    _name: str

    def __init__(self, content: str, log: Logger) -> None:
        super().__init__(BlockTypes.Variable, content, log)


logger: logging.Logger = logging.getLogger(__name__)

VAR_BLOCK_REGEX = r"^[${1}](?P<name>[0-9A-Za-z_]+)$"

VAR_BLOCK_MATCHER = compile(VAR_BLOCK_REGEX)


class VarBlock(Block):
    """Create a variable block.

    A variable block is used to add a variable to a template.
    It gets rendered from KernelArguments, if the variable is not found
    a warning is logged and an empty string is returned.
    The variable must start with $ and be followed by a valid variable name.
    A valid variable name is a string of letters, numbers and underscores.

    Examples:
        $var
        $test_var

    Args:
        content - str : The content of the variable block, the name of the variable.
        name - str: The name of the variable.

    Raises:
        VarBlockSyntaxError: If the content does not match the variable syntax.

    """

    type: ClassVar[BlockTypes] = BlockTypes.VARIABLE
    name: str = ""

    @model_validator(mode="before")
    @classmethod
    def parse_content(cls, fields: Any) -> Any:
        """Parse the content and extract the name.

        The parsing is based on a regex that returns the name.
        if the 'name' is already present then the parsing is skipped.
        """
        if isinstance(fields, Block) or "name" in fields:
            return fields
        content = fields.get("content", "").strip()
        matches = VAR_BLOCK_MATCHER.match(content)
        if not matches:
            raise VarBlockSyntaxError(content=content)
        if name := matches.groupdict().get("name"):
            fields["name"] = name
        return fields

    def render(self, _: "Kernel", arguments: Optional["KernelArguments"] = None) -> str:
        """Render the variable block with the given arguments.

        If the variable is not found in the arguments, return an empty string.
        """
        if arguments is None:
            return ""
        value = arguments.get(self.name, None)
        if value is None:
            logger.warning(
                f"Variable `{Symbols.VAR_PREFIX}: {self.name}` not found in the KernelArguments"
            )
            return ""
        try:
            return str(value)
        except Exception as e:
            raise VarBlockRenderError(
                f"Block {self.name} failed to be parsed to a string, type is {type(value)}"
            ) from e
from logging import Logger
from re import match as regex_match
from typing import Literal, Optional, Tuple

from semantic_kernel.orchestration.context_variables import ContextVariables
from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.template_engine.blocks.block_types import BlockTypes
from semantic_kernel.template_engine.template_exception import TemplateException
from semantic_kernel.utils.static_property import static_property


class VarBlock(Block):
    _name: str

    def __init__(self, content: str, log: Logger) -> None:
        super().__init__(BlockTypes.Variable, content, log)

    def is_valid(self) -> Tuple[bool, str]:
        error = ""

        if self._content is None:
            error = "This variable's content is None"
        elif self._content.strip() == "":
            error = "This variable's content is empty"
        elif self._content[0] != VarBlock.PREFIX:
            error = f"A variable must start with the symbol {VarBlock.PREFIX}"
        elif not self.is_valid_var_name(self.name):
            error = (
                f"The variable name '{self.name}' contains invalid characters."
                " Only alphanumeric characters and underscores are allowed."
            )

        if error != "":
            self._log.error(error)
            return False, error

        return True, ""

    def render(self, variables: Optional[ContextVariables]) -> str:
        if variables is None:
            return ""

        if self.name is not None and self.name.strip() != "":
            exists, value = variables.get(self.name)

            if not exists:
                self._log.warning(f"Variable {VarBlock.PREFIX}{self.name} not found")

            return value if exists else ""

        self._log.error("Variable rendering failed, the variable name is None or empty")
        raise TemplateException(
            TemplateException.ErrorCodes.SyntaxError,
            "Variable rendering failed, the variable name is None or empty",
        )

    @property
    def name(self) -> str:
        if self._content is None or len(self._content) < 2:
            return ""

        return self._content[1:]

            if not exists:
                self._log.warning(f"Variable {VarBlock.PREFIX}{self.name} not found")

            return value if exists else ""

        self._log.error("Variable rendering failed, the variable name is None or empty")
        raise TemplateException(
            TemplateException.ErrorCodes.SyntaxError,
            "Variable rendering failed, the variable name is None or empty",
        )

    @property
    def name(self) -> str:
        if self._content is None or len(self._content) < 2:
            return ""

        return self._content[1:]

    @staticmethod
    def has_var_prefix(text: str) -> bool:
        return text is not None and text.strip() != "" and text[0] == VarBlock.PREFIX

    @staticmethod
    def is_valid_var_name(text: str) -> bool:
        return regex_match(r"^[a-zA-Z0-9_]*$", text) is not None

    @static_property
    def PREFIX() -> Literal["$"]:
        return "$"

    @staticmethod
    def has_var_prefix(text: str) -> bool:
        return text is not None and text.strip() != "" and text[0] == VarBlock.PREFIX

    @staticmethod
    def is_valid_var_name(text: str) -> bool:
        return regex_match(r"^[a-zA-Z0-9_]*$", text) is not None

    @static_property
    def PREFIX() -> Literal["$"]:
        return "$"

logger: logging.Logger = logging.getLogger(__name__)

VAR_BLOCK_REGEX = r"^[${1}](?P<name>[0-9A-Za-z_]+)$"

VAR_BLOCK_MATCHER = compile(VAR_BLOCK_REGEX)


class VarBlock(Block):
    """Create a variable block.

    A variable block is used to add a variable to a template.
    It get's rendered from KernelArguments, if the variable is not found
    a warning is logged and an empty string is returned.
    The variable must start with $ and be followed by a valid variable name.
    A valid variable name is a string of letters, numbers and underscores.

    Examples:
        $var
        $test_var

    Args:
        content - str : The content of the variable block, the name of the variable.
        name - str: The name of the variable.

    Raises:
        VarBlockSyntaxError: If the content does not match the variable syntax.

    """

    type: ClassVar[BlockTypes] = BlockTypes.VARIABLE
    name: Optional[str] = ""

    @model_validator(mode="before")
    @classmethod
    def parse_content(cls, fields: Any) -> Any:
        """Parse the content and extract the name.

        The parsing is based on a regex that returns the name.
        if the 'name' is already present then the parsing is skipped.
        """
        if isinstance(fields, Block) or "name" in fields:
            return fields
        content = fields.get("content", "").strip()
        matches = VAR_BLOCK_MATCHER.match(content)
        if not matches:
            raise VarBlockSyntaxError(content=content)
        if name := matches.groupdict().get("name"):
            fields["name"] = name
        return fields

    def render(self, _: "Kernel", arguments: Optional["KernelArguments"] = None) -> str:
        """Render the variable block with the given arguments.
        If the variable is not found in the arguments, return an empty string."""
        if arguments is None:
            return ""
        value = arguments.get(self.name, None)
        if value is None:
            logger.warning(f"Variable `{Symbols.VAR_PREFIX}{self.name}` not found in the KernelArguments")

        return str(value) if value else ""
from semantic_kernel.template_engine.blocks.symbols import Symbols
from semantic_kernel.template_engine.protocols.text_renderer import TextRenderer


class VarBlock(Block, TextRenderer):
    def __init__(self, content: Optional[str] = None, log: Optional[Logger] = None):
        super().__init__(content=content and content.strip(), log=log)

        if len(self.content) < 2:
            err = "The variable name is empty"
            self.log.error(err)
            self.name = ""
            return

        self.name = self.content[1:]

    @property
    def type(self) -> BlockTypes:
        return BlockTypes.VARIABLE

    def is_valid(self) -> Tuple[bool, str]:
        if not self.content:
            error_msg = (
                f"A variable must start with the symbol {Symbols.VAR_PREFIX} "
                "and have a name"
            )
            self.log.error(error_msg)
            return False, error_msg

        if self.content[0] != Symbols.VAR_PREFIX:
            error_msg = f"A variable must start with the symbol {Symbols.VAR_PREFIX}"
            self.log.error(error_msg)
            return False, error_msg

        if len(self.content) < 2:
            error_msg = "The variable name is empty"
            self.log.error(error_msg)
            return False, error_msg

        if not re_match(r"^[a-zA-Z0-9_]*$", self.name):
            error_msg = (
                f"The variable name '{self.name}' contains invalid characters. "
                "Only alphanumeric chars and underscore are allowed."
            )
            self.log.error(error_msg)
            return False, error_msg

        return True, ""

    def render(self, variables: Optional[ContextVariables] = None) -> str:
        if variables is None:
            return ""

        if not self.name:
            error_msg = "Variable rendering failed, the variable name is empty"
            self.log.error(error_msg)
            raise ValueError(error_msg)

        exists, value = variables.get(self.name)
        if not exists:
            self.log.warning(f"Variable `{Symbols.VAR_PREFIX}{self.name}` not found")

        return value if exists else ""
