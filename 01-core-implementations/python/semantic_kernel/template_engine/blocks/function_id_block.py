# Copyright (c) Microsoft. All rights reserved.

import logging
from re import compile
from typing import TYPE_CHECKING, Any, ClassVar

from pydantic import model_validator

from semantic_kernel.exceptions import FunctionIdBlockSyntaxError
from semantic_kernel.template_engine.blocks.block import Block
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Optional, Tuple

from pydantic import model_validator

from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.template_engine.blocks.block_errors import FunctionIdBlockSyntaxError
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Optional, Tuple

from pydantic import model_validator

from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.template_engine.blocks.block_errors import FunctionIdBlockSyntaxError
from semantic_kernel.template_engine.blocks.block_types import BlockTypes

if TYPE_CHECKING:
    from semantic_kernel.functions.kernel_arguments import KernelArguments
    from semantic_kernel.kernel import Kernel

logger: logging.Logger = logging.getLogger(__name__)

FUNCTION_ID_BLOCK_REGEX = (
    r"^((?P<plugin>[0-9A-Za-z_]+)[.])?(?P<function>[0-9A-Za-z_]+)$"
)

logger: logging.Logger = logging.getLogger(__name__)

logger: logging.Logger = logging.getLogger(__name__)

FUNCTION_ID_BLOCK_REGEX = (
    r"^((?P<plugin>[0-9A-Za-z_]+)[.])?(?P<function>[0-9A-Za-z_]+)$"
)

FUNCTION_ID_BLOCK_MATCHER = compile(FUNCTION_ID_BLOCK_REGEX)

FUNCTION_ID_BLOCK_REGEX = (
    r"^((?P<plugin>[0-9A-Za-z_]+)[.])?(?P<function>[0-9A-Za-z_]+)$"
)
FUNCTION_ID_BLOCK_REGEX = r"^((?P<plugin>[0-9A-Za-z_]+)[.])?(?P<function>[0-9A-Za-z_]+)$"

FUNCTION_ID_BLOCK_MATCHER = compile(FUNCTION_ID_BLOCK_REGEX)

class FunctionIdBlock(Block):
    """Block to represent a function id. It can be used to call a function from a plugin.

    The content is parsed using a regex, that returns either a plugin and
    function name or just a function name, depending on the content.

    Anything other than that and a ValueError is raised.
    Anything other than that and a ValueError is raised.

    Args:
        content (str): The content of the block.
        function_name (Optional[str], optional): The function name.
        plugin_name (Optional[str], optional): The plugin name.

    Raises:
        ValueError: If the content does not have valid syntax.
    """

    type: ClassVar[BlockTypes] = BlockTypes.FUNCTION_ID
    function_name: str = ""
    plugin_name: str | None = None

logger: logging.Logger = logging.getLogger(__name__)

FUNCTION_ID_BLOCK_REGEX = (
    r"^((?P<plugin>[0-9A-Za-z_]+)[.])?(?P<function>[0-9A-Za-z_]+)$"
)
FUNCTION_ID_BLOCK_REGEX = r"^((?P<plugin>[0-9A-Za-z_]+)[.])?(?P<function>[0-9A-Za-z_]+)$"

FUNCTION_ID_BLOCK_MATCHER = compile(FUNCTION_ID_BLOCK_REGEX)


class FunctionIdBlock(Block):
    """Block to represent a function id. It can be used to call a function from a plugin.

    The content is parsed using a regex, that returns either a plugin and
    function name or just a function name, depending on the content.

    Anything other than that and a ValueError is raised.

    Args:
        content (str): The content of the block.
        function_name (Optional[str], optional): The function name.
        plugin_name (Optional[str], optional): The plugin name.

    Raises:
        ValueError: If the content does not have valid syntax.
    """

    type: ClassVar[BlockTypes] = BlockTypes.FUNCTION_ID
    function_name: str = ""
    plugin_name: str | None = None

    function_name: str = ""
    plugin_name: str | None = None

    function_name: str = ""
    plugin_name: str | None = None

    @model_validator(mode="before")
    @classmethod
    def parse_content(cls, fields: Any) -> dict[str, Any]:
        """Parse the content of the function id block and extract the plugin and function name.

        If both are present in the fields, return the fields as is.
        Otherwise, use the regex to extract the plugin and function name.
    function_name: Optional[str] = ""
    plugin_name: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def parse_content(cls, fields: Dict[str, Any]) -> Dict[str, Any]:
        """Parse the content of the function id block and extract the plugin and function name.

        If both are present in the fields, return the fields as is.
        Otherwise use the regex to extract the plugin and function name.
        """
        if isinstance(fields, dict):
            if "plugin_name" in fields and "function_name" in fields:
                return fields
            content = fields.get("content", "").strip()
            matches = FUNCTION_ID_BLOCK_MATCHER.match(content)
            if not matches:
                raise FunctionIdBlockSyntaxError(content=content)
            if plugin := matches.groupdict().get("plugin"):
                fields["plugin_name"] = plugin
            fields["function_name"] = matches.group("function")
        return fields

    def render(self, *_: "Kernel | KernelArguments | None") -> str:
        """Render the function id block."""
    def render(self, *_: "Kernel | KernelArguments | None") -> str:
        """Render the function id block."""
    def render(self, *_: "Kernel | KernelArguments | None") -> str:
        """Render the function id block."""
    def render(self, *_: Tuple["Kernel", Optional["KernelArguments"]]) -> str:
        return self.content
from logging import Logger
from re import match as re_match
from typing import Optional, Tuple

from semantic_kernel.orchestration.context_variables import ContextVariables
from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.template_engine.blocks.block_types import BlockTypes
from semantic_kernel.template_engine.protocols.text_renderer import TextRenderer


class FunctionIdBlock(Block, TextRenderer):
    def __init__(self, content: Optional[str] = None, log: Optional[Logger] = None):
        super().__init__(content=content and content.strip(), log=log)

        function_name_parts = self.content.split(".")
        if len(function_name_parts) > 2:
            self.log.error(f"Invalid function name `{self.content}`")
            raise ValueError(
                "A function name can contain at most one dot separating "
                "the skill name from the function name"
            )

        if len(function_name_parts) == 2:
            self.skill_name = function_name_parts[0]
            self.function_name = function_name_parts[1]
        else:
            self.skill_name = ""
            self.function_name = self.content

    @property
    def type(self) -> BlockTypes:
        return BlockTypes.FUNCTION_ID

    def is_valid(self) -> Tuple[bool, str]:
        if self.content is None or len(self.content) == 0:
            error_msg = "The function identifier is empty"
            return False, error_msg

        if not re_match(r"^[a-zA-Z0-9_.]*$", self.content):
            # NOTE: this is not quite the same as
            # utils.validation.validate_function_name
            error_msg = (
                f"The function identifier '{self.content}' contains invalid "
                "characters. Only alphanumeric chars, underscore and a single "
                "dot are allowed."
            )
            return False, error_msg

        if self._has_more_than_one_dot(self.content):
            error_msg = (
                "The function identifier can contain max one '.' "
                "char separating skill name from function name"
            )
            return False, error_msg

        return True, ""

    def render(self, _: Optional[ContextVariables] = None) -> str:
        return self.content

    def _has_more_than_one_dot(self, value: Optional[str]) -> bool:
        if value is None or len(value) < 2:
            return False

        count = 0
        for char in value:
            if char == ".":
                count += 1
                if count > 1:
                    return True

        return False
