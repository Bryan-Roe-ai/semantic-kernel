# Copyright (c) Microsoft. All rights reserved.

from abc import ABC, abstractmethod
from typing import Any, TypeVar

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from typing import Annotated, Any, TypeVar

from abc import ABC, abstractmethod
from typing import Any, TypeVar

from abc import ABC, abstractmethod
from typing import Any, TypeVar

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from typing import Any, TypeVar

from pydantic import Field

from semantic_kernel.kernel_pydantic import KernelBaseModel

_T = TypeVar("_T", bound="KernelContent")

class KernelContent(KernelBaseModel, ABC):
    """Base class for all kernel contents."""

    inner_content: Any | None = None
    # NOTE: if you wish to hold on to the inner content, you are responsible
    # for saving it before serializing the content/chat history as it won't be included.
    inner_content: Any | None = Field(None, exclude=True)
    inner_content: Annotated[Any | None, Field(exclude=True)] = None

_T = TypeVar("_T", bound="KernelContent")

_T = TypeVar("_T", bound="KernelContent")

_T = TypeVar("_T", bound="KernelContent")

_T = TypeVar("_T", bound="KernelContent")

_T = TypeVar("_T", bound="KernelContent")

class KernelContent(KernelBaseModel, ABC):
    """Base class for all kernel contents."""

    inner_content: Any | None = None

    ai_model_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @abstractmethod
    def __str__(self) -> str:
        """Return the string representation of the content."""

    @abstractmethod
    def to_element(self) -> Any:
        """Convert the instance to an Element."""

    @classmethod
    @abstractmethod
    def from_element(cls: type[_T], element: Any) -> _T:
        """Create an instance from an Element."""

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Convert the instance to a dictionary."""

    inner_content: Optional[Any] = None
    ai_model_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @abstractmethod
    def __str__(self) -> str:
        pass

