# Copyright (c) Microsoft. All rights reserved.

import logging
<<<<<<< main
from typing import TYPE_CHECKING, ClassVar, Optional
=======
from typing import TYPE_CHECKING, ClassVar, Optional, Tuple
>>>>>>> ms/small_fixes

from pydantic import field_validator

from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.template_engine.blocks.block_types import BlockTypes

if TYPE_CHECKING:
    from semantic_kernel.functions.kernel_arguments import KernelArguments
    from semantic_kernel.kernel import Kernel

logger: logging.Logger = logging.getLogger(__name__)


class TextBlock(Block):
<<<<<<< main
    """A block with text content."""

=======
>>>>>>> ms/small_fixes
    type: ClassVar[BlockTypes] = BlockTypes.TEXT

    @field_validator("content", mode="before")
    @classmethod
    def content_strip(cls, content: str):
<<<<<<< main
        """Strip the content of the text block.

        Overload strip method, text blocks are not stripped.
        """
=======
        # overload strip method text blocks are not stripped.
>>>>>>> ms/small_fixes
        return content

    @classmethod
    def from_text(
        cls,
<<<<<<< main
        text: str | None = None,
        start_index: int | None = None,
        stop_index: int | None = None,
    ):
        """Create a text block from a string."""
=======
        text: Optional[str] = None,
        start_index: Optional[int] = None,
        stop_index: Optional[int] = None,
    ):
>>>>>>> ms/small_fixes
        if text is None:
            return cls(content="")
        if start_index is not None and stop_index is not None:
            if start_index > stop_index:
                raise ValueError(
                    f"start_index ({start_index}) must be less than stop_index ({stop_index})"
                )

            if start_index < 0:
                raise ValueError(f"start_index ({start_index}) must be greater than 0")

            text = text[start_index:stop_index]
        elif start_index is not None:
            text = text[start_index:]
        elif stop_index is not None:
            text = text[:stop_index]

        return cls(content=text)

<<<<<<< main
    def render(self, *_: tuple[Optional["Kernel"], Optional["KernelArguments"]]) -> str:
        """Render the text block."""
        return self.content
from logging import Logger
from typing import Optional, Tuple

from semantic_kernel.orchestration.context_variables import ContextVariables
from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.template_engine.blocks.block_types import BlockTypes


class TextBlock(Block):
    def __init__(self, content: str, log: Logger) -> None:
        super().__init__(BlockTypes.Text, content, log)

    def is_valid(self) -> Tuple[bool, str]:
        return True, ""

    def render(self, _: Optional[ContextVariables]) -> str:
        return self._content
=======
    def render(self, *_: Tuple[Optional["Kernel"], Optional["KernelArguments"]]) -> str:
        return self.content
>>>>>>> ms/small_fixes
