# Copyright (c) Microsoft. All rights reserved.

<<<<<<< HEAD
from abc import ABC
from typing import TYPE_CHECKING, Annotated

from pydantic import Field, StringConstraints

from semantic_kernel.kernel_pydantic import KernelBaseModel

if TYPE_CHECKING:
    from semantic_kernel.connectors.ai.prompt_execution_settings import (
        PromptExecutionSettings,
    )

=======
import sys
from abc import ABC
from typing import Optional

if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated

from pydantic import Field, StringConstraints

from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from semantic_kernel.kernel_pydantic import KernelBaseModel

>>>>>>> f40c1f2075e2443c31c57c34f5f66c2711a8db75

class AIServiceClientBase(KernelBaseModel, ABC):
    """Base class for all AI Services.

<<<<<<< HEAD
    Has an ai_model_id and service_id, any other fields have to be defined by the subclasses.
=======
    Has a ai_model_id and service_id, any other fields have to be defined by the subclasses.
>>>>>>> f40c1f2075e2443c31c57c34f5f66c2711a8db75

    The ai_model_id can refer to a specific model, like 'gpt-35-turbo' for OpenAI,
    or can just be a string that is used to identify the model in the service.

    The service_id is used in Semantic Kernel to identify the service, if empty the ai_model_id is used.
    """

    ai_model_id: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    service_id: str = Field("")

<<<<<<< HEAD
    def model_post_init(self, __context: object | None = None):
=======
    def model_post_init(self, __context: Optional[object] = None):
>>>>>>> f40c1f2075e2443c31c57c34f5f66c2711a8db75
        """Update the service_id if it is not set."""
        if not self.service_id:
            self.service_id = self.ai_model_id

<<<<<<< HEAD
    # Override this in subclass to return the proper prompt execution type the
    # service is expecting.
    def get_prompt_execution_settings_class(self) -> type["PromptExecutionSettings"]:
        """Get the request settings class."""
        from semantic_kernel.connectors.ai.prompt_execution_settings import (
            PromptExecutionSettings,
        )

        return PromptExecutionSettings
    def get_prompt_execution_settings_class(self) -> type["PromptExecutionSettings"]:
        """Get the request settings class.

        Overwrite this in subclass to return the proper prompt execution type the
        service is expecting.
        """
        return PromptExecutionSettings  # pragma: no cover

    def instantiate_prompt_execution_settings(
        self, **kwargs
    ) -> "PromptExecutionSettings":
=======
    def get_prompt_execution_settings_class(self) -> "PromptExecutionSettings":
        """Get the request settings class."""
        return PromptExecutionSettings  # pragma: no cover

    def instantiate_prompt_execution_settings(self, **kwargs) -> "PromptExecutionSettings":
>>>>>>> f40c1f2075e2443c31c57c34f5f66c2711a8db75
        """Create a request settings object.

        All arguments are passed to the constructor of the request settings object.
        """
        return self.get_prompt_execution_settings_class()(**kwargs)

<<<<<<< HEAD
    def get_prompt_execution_settings_from_settings(
        self, settings: "PromptExecutionSettings"
    ) -> "PromptExecutionSettings":
        """Get the request settings from a settings object."""
        prompt_execution_settings_type = self.get_prompt_execution_settings_class()
        if isinstance(settings, prompt_execution_settings_type):
            return settings

        return prompt_execution_settings_type.from_prompt_execution_settings(settings)
=======
    def get_prompt_execution_settings_from_settings(self, settings: PromptExecutionSettings) -> PromptExecutionSettings:
        """Get the request settings from a settings object."""
        return self.get_prompt_execution_settings_class().from_prompt_execution_settings(settings)
>>>>>>> f40c1f2075e2443c31c57c34f5f66c2711a8db75
