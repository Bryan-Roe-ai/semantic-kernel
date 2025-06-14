# Copyright (c) Microsoft. All rights reserved.
import logging
from collections.abc import MutableMapping, MutableSequence, Sequence
from typing import TypeVar

from pydantic import Field, field_validator, model_validator

from semantic_kernel.connectors.ai.prompt_execution_settings import (
    PromptExecutionSettings,
)
from semantic_kernel.const import DEFAULT_SERVICE_NAME
from semantic_kernel.functions.kernel_parameter_metadata import KernelParameterMetadata
from semantic_kernel.kernel_pydantic import KernelBaseModel
from semantic_kernel.prompt_template.const import (
    KERNEL_TEMPLATE_FORMAT_NAME,
    TEMPLATE_FORMAT_TYPES,
)
from semantic_kernel.prompt_template.input_variable import InputVariable

PromptExecutionSettingsT = TypeVar(
    "PromptExecutionSettingsT", bound=PromptExecutionSettings
)
import json
import logging
from typing import Dict, List, Optional, TypeVar, Union

from pydantic import Field, field_validator
from typing_extensions import Literal

from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from semantic_kernel.functions.kernel_parameter_metadata import KernelParameterMetadata
from semantic_kernel.kernel_pydantic import KernelBaseModel
from semantic_kernel.prompt_template.input_variable import InputVariable

PromptExecutionSettingsT = TypeVar("PromptExecutionSettingsT", bound=PromptExecutionSettings)

logger: logging.Logger = logging.getLogger(__name__)

_T = TypeVar("_T", bound="PromptTemplateConfig")

class PromptTemplateConfig(KernelBaseModel):
    """Configuration for a prompt template.

    Args:
        name: The name of the prompt template.
        description: The description of the prompt template.
        template: The template for the prompt.
        template_format: The format of the template, should be 'semantic-kernel', 'jinja2' or 'handlebars'.
        input_variables: The input variables for the prompt.
        allow_dangerously_set_content (bool = False): Allow content without encoding throughout, this overrides
            the same settings in the prompt template config and input variables.
            This reverts the behavior to unencoded input.
        execution_settings: The execution settings for the prompt.

    """

    name: str = ""
    description: str | None = ""
    template: str | None = None
    template_format: TEMPLATE_FORMAT_TYPES = KERNEL_TEMPLATE_FORMAT_NAME
    input_variables: MutableSequence[InputVariable] = Field(default_factory=list)
    allow_dangerously_set_content: bool = False
    execution_settings: MutableMapping[str, PromptExecutionSettings] = Field(default_factory=dict)

    @model_validator(mode="after")
    def check_input_variables(self):
        """Verify that input variable default values are string only."""
        for variable in self.input_variables:
            if variable.default and not isinstance(variable.default, str):
                raise TypeError(
                    f"Default value for input variable {variable.name} must be a string."
                )
        return self
    name: Optional[str] = ""
    description: Optional[str] = ""
    template: Optional[str] = None
    template_format: Optional[str] = "semantic-kernel"
    input_variables: List[InputVariable] = Field(default_factory=list)
    execution_settings: Dict[str, PromptExecutionSettings] = Field(default_factory=dict)

    @field_validator("execution_settings", mode="before")
    @classmethod
    def rewrite_execution_settings(
        cls,
        settings: None | (
            PromptExecutionSettings
            | list[PromptExecutionSettings]
            | dict[str, PromptExecutionSettings]
        ),
        settings: PromptExecutionSettings | list[PromptExecutionSettings] | dict[str, PromptExecutionSettings] | None,
    ) -> dict[str, PromptExecutionSettings]:
        settings: Optional[
            Union[PromptExecutionSettings, List[PromptExecutionSettings], Dict[str, PromptExecutionSettings]]
        ],
    ) -> Dict[str, PromptExecutionSettings]:

        settings: PromptExecutionSettings
        | Sequence[PromptExecutionSettings]
        | MutableMapping[str, PromptExecutionSettings]
        | None,
    ) -> MutableMapping[str, PromptExecutionSettings]:
        """Rewrite execution settings to a dictionary."""
        if not settings:
            return {}
        if isinstance(settings, PromptExecutionSettings):
            return {settings.service_id or DEFAULT_SERVICE_NAME: settings}
        if isinstance(settings, Sequence):
            return {s.service_id or DEFAULT_SERVICE_NAME: s for s in settings}
        return settings

    def add_execution_settings(
        self, settings: PromptExecutionSettings, overwrite: bool = True
    ) -> None:
        """Add execution settings to the prompt template."""
        if settings.service_id in self.execution_settings and not overwrite:
            return
        self.execution_settings[settings.service_id or DEFAULT_SERVICE_NAME] = settings
        logger.warning("Execution settings already exist and overwrite is set to False")

    def get_kernel_parameter_metadata(self) -> list[KernelParameterMetadata]:
            return {settings.service_id or "default": settings}
        if isinstance(settings, list):
            return {s.service_id or "default": s for s in settings}
        return settings

    def add_execution_settings(self, settings: PromptExecutionSettings, overwrite: bool = True) -> None:
        """Add execution settings to the prompt template."""
        if settings.service_id in self.execution_settings and not overwrite:
            return
        self.execution_settings[settings.service_id or "default"] = settings
        logger.warning("Execution settings already exist and overwrite is set to False")

    def get_kernel_parameter_metadata(self) -> List[KernelParameterMetadata]:
    def get_kernel_parameter_metadata(self) -> Sequence[KernelParameterMetadata]:
        """Get the kernel parameter metadata for the input variables."""
        return [
            KernelParameterMetadata(
                name=variable.name,
                description=variable.description,
                default_value=variable.default,
                type_=variable.json_schema,  # TODO (moonbox3): update to handle complex JSON schemas # type: ignore
                is_required=variable.is_required,
                type_=variable.json_schema,  # TODO (moonbox3): update to handle complex JSON schemas
                is_required=variable.is_required,
                type_=variable.json_schema,  # TODO (moonbox3): update to handle complex JSON schemas
                is_required=variable.is_required,
                type_=variable.json_schema,  # TODO (moonbox3): update to handle complex JSON schemas
                is_required=variable.is_required,
                type_=variable.json_schema,  # TODO (moonbox3): update to handle complex JSON schemas
                is_required=variable.is_required,
                type_=variable.json_schema,  # TODO: update to handle complex JSON schemas
                required=variable.is_required,
                expose=True,
            )
            for variable in self.input_variables
        ]

    @classmethod
    def from_json(cls: type[_T], json_str: str) -> _T:
        """Create a PromptTemplateConfig instance from a JSON string."""
        if not json_str:
            raise ValueError("json_str is empty")
        try:
            return cls.model_validate_json(json_str)
        except Exception as exc:
            raise ValueError(
                "Unable to deserialize PromptTemplateConfig from the "
                f"specified JSON string: {json_str} with exception: {exc}"
            ) from exc

        try:
            parsed_json = json.loads(json_str)
            config = PromptTemplateConfig(**parsed_json)
        except Exception as e:
            raise ValueError(
                "Unable to deserialize PromptTemplateConfig from the "
                f"specified JSON string: {json_str} with exception: {e}"
            )

        # Verify that input variable default values are string only
        for variable in config.input_variables:
            if variable.default and not isinstance(variable.default, str):
                raise ValueError(f"Default value for input variable {variable.name} must be a string for {config.name}")

        return config

    @classmethod
    def restore(
        cls: type[_T],
        name: str,
        description: str,
        template: str,
        template_format: TEMPLATE_FORMAT_TYPES = KERNEL_TEMPLATE_FORMAT_NAME,
        input_variables: MutableSequence[InputVariable] | None = None,
        execution_settings: MutableMapping[str, PromptExecutionSettings] | None = None,
        allow_dangerously_set_content: bool = False,
        template_format: Literal["semantic-kernel"] = "semantic-kernel",
        input_variables: List[InputVariable] = [],
        execution_settings: Dict[str, PromptExecutionSettings] = {},
    ) -> "PromptTemplateConfig":

        """Restore a PromptTemplateConfig instance from the specified parameters.

        Args:
            name: The name of the prompt template.
            description: The description of the prompt template.
            template: The template for the prompt.
            template_format: The format of the template, should be 'semantic-kernel', 'jinja2' or 'handlebars'.
            input_variables: The input variables for the prompt.
            execution_settings: The execution settings for the prompt.
            allow_dangerously_set_content: Allow content without encoding.
            input_variables: The input variables for the prompt.
            execution_settings: The execution settings for the prompt.

        Returns:
            A new PromptTemplateConfig instance.
        """
        return cls(
            name=name,
            description=description,
            template=template,
            template_format=template_format,
            input_variables=input_variables or [],
            execution_settings=execution_settings or {},
            allow_dangerously_set_content=allow_dangerously_set_content,
        )
