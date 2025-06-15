# Copyright (c) Microsoft. All rights reserved.

from abc import abstractmethod
from typing import TYPE_CHECKING, Optional, Protocol, runtime_checkable

if TYPE_CHECKING:
    from semantic_kernel import Kernel
    from semantic_kernel.functions.kernel_arguments import KernelArguments
from typing import Optional, Protocol, runtime_checkable

from semantic_kernel.orchestration.context_variables import ContextVariables


@runtime_checkable
class TextRenderer(Protocol):
    """Protocol for static (text) blocks that don't need async rendering."""

    def render(
        self, kernel: "Kernel", arguments: Optional["KernelArguments"] = None
    ) -> str:
    @abstractmethod
    def render(self, kernel: "Kernel", arguments: Optional["KernelArguments"] = None) -> str:
        """Render the block using only the given variables.
    def render(self, kernel: "Kernel", arguments: Optional["KernelArguments"] = None) -> str:
        """
        Render the block using only the given variables.
    """
    Protocol for static (text) blocks that don't need async rendering.
    """

    def render(self, variables: Optional[ContextVariables] = None) -> str:
        """
        Render the block using only the given variables.

        :param variables: Optional variables used to render the block
        :return: Rendered content
        """
        ...
