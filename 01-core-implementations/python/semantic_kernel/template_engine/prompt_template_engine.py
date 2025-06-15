# Copyright (c) Microsoft. All rights reserved.

from logging import Logger
from typing import List, Optional

from semantic_kernel.orchestration.context_variables import ContextVariables
from semantic_kernel.orchestration.sk_context import SKContext
from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.template_engine.blocks.block_types import BlockTypes
from semantic_kernel.template_engine.blocks.code_block import CodeBlock
from semantic_kernel.template_engine.blocks.text_block import TextBlock
from semantic_kernel.template_engine.blocks.var_block import VarBlock
from semantic_kernel.template_engine.prompt_template_engine_base import (
    PromptTemplateEngineBase,
)
from semantic_kernel.template_engine.template_exception import TemplateException
from semantic_kernel.utils.null_logger import NullLogger


class PromptTemplateEngine(PromptTemplateEngineBase):
    _log: Logger

    def __init__(self, log: Optional[Logger] = None) -> None:
        self._log = log if log is not None else NullLogger()

    def extract_blocks(
        self, template_text: Optional[str], validate: bool = True
    ) -> List[Block]:
        self._log.debug(f"Extracting blocks from template: {template_text}")
        blocks = self._tokenize_internal(template_text)
        if validate:
            PromptTemplateEngine.validate_blocks_syntax(blocks)
        return blocks

    async def render_async(self, template_text: str, context: SKContext) -> str:
        self._log.debug(f"Rendering string template: {template_text}")
from semantic_kernel.template_engine.blocks.text_block import TextBlock
from semantic_kernel.template_engine.protocols.code_renderer import CodeRenderer
from semantic_kernel.template_engine.protocols.prompt_templating_engine import (
    PromptTemplatingEngine,
)
from semantic_kernel.template_engine.protocols.text_renderer import TextRenderer
from semantic_kernel.template_engine.template_tokenizer import TemplateTokenizer
from semantic_kernel.utils.null_logger import NullLogger


class PromptTemplateEngine(PromptTemplatingEngine):
    def __init__(self, logger: Optional[Logger] = None) -> None:
        self._logger = logger or NullLogger()
        self._tokenizer = TemplateTokenizer(self._logger)

    def extract_blocks(
        self, template_text: Optional[str] = None, validate: bool = True
    ) -> List[Block]:
        """
        Given a prompt template string, extract all the blocks
        (text, variables, function calls).

        :param template_text: Prompt template (see skprompt.txt files)
        :param validate: Whether to validate the blocks syntax, or just
            return the blocks found, which could contain invalid code
        :return: A list of all the blocks, ie the template tokenized in
            text, variables and function calls
        """
        self._logger.debug(f"Extracting blocks from template: {template_text}")
        blocks = self._tokenizer.tokenize(template_text)

        if validate:
            for block in blocks:
                is_valid, error_message = block.is_valid()
                if not is_valid:
                    raise ValueError(error_message)

        return blocks

    async def render_async(self, template_text: str, context: SKContext) -> str:
        """
        Given a prompt template, replace the variables with their values
        and execute the functions replacing their reference with the
        function result.

        :param template_text: Prompt template (see skprompt.txt files)
        :param context: Access into the current kernel execution context
        :return: The prompt template ready to be used for an AI request
        """
        self._logger.debug(f"Rendering string template: {template_text}")
        blocks = self.extract_blocks(template_text)
        return await self.render_blocks_async(blocks, context)

    async def render_blocks_async(self, blocks: List[Block], context: SKContext) -> str:
        self._log.debug(f"Rendering list of {len(blocks)} blocks")
        result = ""
        for block in blocks:
            if block.type == BlockTypes.Text:
                result += block.content
                continue

            if block.type == BlockTypes.Variable:
                result += block.render(context.variables)
                continue

            if block.type == BlockTypes.Code:
                result += await block.render_code_async(context)
                continue

            raise NotImplementedError(f"Block type {block.type} is not supported")

        self._log.debug(f"Rendered prompt: {result}")
        return result

    def render_variables(
        self, blocks: List[Block], context: Optional[ContextVariables]
    ) -> List[Block]:
        self._log.debug("Rendering variables")
        return list(
            [
                block
                if block.type != BlockTypes.Variable
                else TextBlock(block.render(context), self._log)
                for block in blocks
            ]
        )

    async def render_code_async(
        self, blocks: List[Block], context: SKContext
    ) -> List[Block]:
        self._log.debug("Rendering code")

        updated_blocks = []
        for block in blocks:
            if block.type != BlockTypes.Code:
                updated_blocks.append(block)
                continue

            updated_blocks.append(
                TextBlock(await block.render_code_async(context), self._log)
            )

        return updated_blocks

    @staticmethod
    def validate_blocks_syntax(blocks: List[Block]) -> None:
        for block in blocks:
            is_valid, message = block.is_valid()
            if not is_valid:
                raise TemplateException(
                    TemplateException.ErrorCodes.SyntaxError, message
                )

    def _tokenize_internal(self, template: Optional[str]) -> List[Block]:
        if template is None or template.strip() == "":
            return [TextBlock("", self._log)]

        STARTER, ENDER = "{", "}"
        # An empty block consists of 4 chars: "{{}}"
        EMPTY_CODE_BLOCK_LENGTH = 4
        # A block shorter than 5 chars is either empty
        # or invalid, e.g. "{{ }}" and "{{$}}"
        MIN_CODE_BLOCK_LENGTH = EMPTY_CODE_BLOCK_LENGTH + 1

        if len(template) < MIN_CODE_BLOCK_LENGTH:
            return [TextBlock(template, self._log)]

        blocks = []

        cursor = 0
        end_of_last_block = 0

        start_pos = 0
        start_found = False

        while cursor < len(template):
            # Utility function to get the char at the given offset
            # (relative to the current cursor position)
            def _get_char(offset: int = 0) -> str:
                return template[cursor + offset]

            # When '{{' is found
            if _get_char() == STARTER and _get_char(1) == STARTER:
                start_pos = cursor
                start_found = True
            # When '}}' is found
            elif start_found and _get_char() == ENDER and _get_char(1) == ENDER:
                # If there is plain text between the current
                # var/code block and the previous one, capture
                # that as a text block
                if start_pos > end_of_last_block:
                    blocks.append(
                        TextBlock(template[end_of_last_block:start_pos], self._log)
                    )

                # Skip ahead of the second '}' of '}}'
                cursor += 1

                # Extract raw block
                content_with_delims = template[start_pos : cursor + 1]

                # Remove the '{{' and '}}' delimiters and trim
                content_without_delims = content_with_delims[
                    len(STARTER + STARTER) : -len(ENDER + ENDER)
                ].strip()

                if len(content_without_delims) == 0:
                    blocks.append(TextBlock(content_with_delims, self._log))
                else:
                    if VarBlock.has_var_prefix(content_without_delims):
                        blocks.append(VarBlock(content_without_delims, self._log))
                    else:
                        blocks.append(CodeBlock(content_without_delims, self._log))

                # Update the end of the last block
                end_of_last_block = cursor + 1
                start_found = False

            # Move the cursor forward
            cursor += 1

        # If there is plain text after the last block, capture that as a text block
        if end_of_last_block < len(template):
            blocks.append(
                TextBlock(template[end_of_last_block : len(template)], self._log)
            )

        return blocks
        """
        Given a list of blocks render each block and compose the final result.

        :param blocks: Template blocks generated by ExtractBlocks
        :param context: Access into the current kernel execution context
        :return: The prompt template ready to be used for an AI request
        """
        self._logger.debug(f"Rendering list of {len(blocks)} blocks")
        rendered_blocks = []
        for block in blocks:
            if isinstance(block, TextRenderer):
                rendered_blocks.append(block.render(context.variables))
            elif isinstance(block, CodeRenderer):
                rendered_blocks.append(await block.render_code_async(context))
            else:
                error = (
                    "unexpected block type, the block doesn't have a rendering "
                    "protocol assigned to it"
                )
                self._logger.error(error)
                raise ValueError(error)

        self._logger.debug(f"Rendered prompt: {''.join(rendered_blocks)}")
        return "".join(rendered_blocks)

    def render_variables(
        self, blocks: List[Block], variables: Optional[ContextVariables] = None
    ) -> List[Block]:
        """
        Given a list of blocks, render the Variable Blocks, replacing
        placeholders with the actual value in memory.

        :param blocks: List of blocks, typically all the blocks found in a template
        :param variables: Container of all the temporary variables known to the kernel
        :return: An updated list of blocks where Variable Blocks have rendered to
            Text Blocks
        """
        self._logger.debug("Rendering variables")

        rendered_blocks = []
        for block in blocks:
            if block.type != BlockTypes.VARIABLE:
                rendered_blocks.append(block)
                continue
            if not isinstance(block, TextRenderer):
                raise ValueError("TextBlock must implement TextRenderer protocol")
            rendered_blocks.append(TextBlock(block.render(variables), log=self._logger))

        return rendered_blocks

    async def render_code_async(
        self, blocks: List[Block], execution_context: SKContext
    ) -> List[Block]:
        """
        Given a list of blocks, render the Code Blocks, executing the
        functions and replacing placeholders with the functions result.

        :param blocks: List of blocks, typically all the blocks found in a template
        :param execution_context: Access into the current kernel execution context
        :return: An updated list of blocks where Code Blocks have rendered to
            Text Blocks
        """
        self._logger.debug("Rendering code")

        rendered_blocks = []
        for block in blocks:
            if block.type != BlockTypes.CODE:
                rendered_blocks.append(block)
                continue
            if not isinstance(block, CodeRenderer):
                raise ValueError("CodeBlock must implement CodeRenderer protocol")
            rendered_blocks.append(
                TextBlock(
                    await block.render_code_async(execution_context), log=self._logger
                )
            )

        return rendered_blocks
