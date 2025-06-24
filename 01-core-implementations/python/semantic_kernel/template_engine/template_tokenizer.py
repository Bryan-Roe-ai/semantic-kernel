#!/usr/bin/env python3
"""
Template Tokenizer module

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

from semantic_kernel.exceptions import (
    BlockSyntaxError,
    CodeBlockTokenError,
    TemplateSyntaxError,
)
from semantic_kernel.template_engine.blocks.block import Block
from typing import List

from typing import List

from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.template_engine.blocks.block_errors import (
    CodeBlockSyntaxError,
    CodeBlockTokenError,
    FunctionIdBlockSyntaxError,
    TemplateSyntaxError,
    ValBlockSyntaxError,
    VarBlockSyntaxError,
)
from logging import Logger
from typing import List

from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.template_engine.blocks.block_types import BlockTypes
from semantic_kernel.template_engine.blocks.code_block import CodeBlock
from semantic_kernel.template_engine.blocks.symbols import Symbols
from semantic_kernel.template_engine.blocks.text_block import TextBlock
from semantic_kernel.template_engine.code_tokenizer import CodeTokenizer

logger: logging.Logger = logging.getLogger(__name__)
from semantic_kernel.utils.null_logger import NullLogger


# BNF parsed by TemplateTokenizer:
# [template]       ::= "" | [block] | [block] [template]
# [block]          ::= [sk-block] | [text-block]
# [sk-block]       ::= "{{" [variable] "}}"
#                      | "{{" [value] "}}"
#                      | "{{" [function-call] "}}"
# [text-block]     ::= [any-char] | [any-char] [text-block]
# [any-char]       ::= any char
class TemplateTokenizer:
    """Tokenize the template text into blocks."""

    @staticmethod
    def tokenize(text: str) -> list[Block]:
        """Tokenize the template text into blocks."""
    @staticmethod
    def tokenize(text: str) -> List[Block]:
    @staticmethod
    def tokenize(text: str) -> List[Block]:
        code_tokenizer = CodeTokenizer()
    def __init__(self, log: Logger = None):
        self.log = log or NullLogger()
        self.code_tokenizer = CodeTokenizer(self.log)

    def tokenize(self, text: str) -> List[Block]:
        # An empty block consists of 4 chars: "{{}}"
        EMPTY_CODE_BLOCK_LENGTH = 4
        # A block shorter than 5 chars is either empty or
        # invalid, e.g. "{{ }}" and "{{$}}"
        MIN_CODE_BLOCK_LENGTH = EMPTY_CODE_BLOCK_LENGTH + 1

        text = text or ""

        # Render None/empty to ""
        if not text:
            return [TextBlock.from_text("")]

        # If the template is "empty" return it as a text block
        if len(text) < MIN_CODE_BLOCK_LENGTH:
            return [TextBlock.from_text(text)]

        blocks: list[Block] = []
        blocks: list[Block] = []
        if not text or text == "":
            return [TextBlock("", log=self.log)]

        # If the template is "empty" return it as a text block
        if len(text) < MIN_CODE_BLOCK_LENGTH:
            return [TextBlock(text, log=self.log)]

        blocks = []
        end_of_last_block = 0
        block_start_pos = 0
        block_start_found = False
        inside_text_value = False
        text_value_delimiter = None
        skip_next_char = False

        for current_char_pos, current_char in enumerate(text[:-1]):
            next_char_pos = current_char_pos + 1
            next_char = text[next_char_pos]
        next_char = text[0]

        for next_char_cursor in range(1, len(text)):
            current_char_pos = next_char_cursor - 1
            cursor = next_char_cursor
            current_char = next_char
            next_char = text[next_char_cursor]

            if skip_next_char:
                skip_next_char = False
                continue

            # When "{{" is found outside a value
            # Note: "{{ {{x}}" => ["{{ ", "{{x}}"]
            if (
                not inside_text_value
                and current_char == Symbols.BLOCK_STARTER
                and next_char == Symbols.BLOCK_STARTER
            ):
                # A block starts at the first "{"
                block_start_pos = current_char_pos
                block_start_found = True

            if not block_start_found:
                continue
            # After having found "{{"
            if inside_text_value:
                # While inside a text value, when the end quote is found
                # If the current char is escaping the next special char we skip
                if current_char == Symbols.ESCAPE_CHAR and next_char in (
                    Symbols.DBL_QUOTE,
                    Symbols.SGL_QUOTE,
                    Symbols.ESCAPE_CHAR,
                ):
                    skip_next_char = True
                    continue

                if current_char == text_value_delimiter:
                    inside_text_value = False
                continue

            # A value starts here
            if current_char in (Symbols.DBL_QUOTE, Symbols.SGL_QUOTE):
                inside_text_value = True
                text_value_delimiter = current_char
                continue
            # If the block ends here
            if current_char == Symbols.BLOCK_ENDER and next_char == Symbols.BLOCK_ENDER:
                blocks.extend(
                    TemplateTokenizer._extract_blocks(
                        text,
                        code_tokenizer,
                        block_start_pos,
                        end_of_last_block,
                        next_char_pos,
                        text, code_tokenizer, block_start_pos, end_of_last_block, next_char_pos
                        text, code_tokenizer, block_start_pos, end_of_last_block, next_char_pos
                    )
                )
                end_of_last_block = next_char_pos + 1
                block_start_found = False

        # If there is something left after the last block, capture it as a TextBlock
        if end_of_last_block < len(text):
            blocks.append(TextBlock.from_text(text, end_of_last_block, len(text)))

        return blocks

    @staticmethod
    def _extract_blocks(
        text: str,
        code_tokenizer: CodeTokenizer,
        block_start_pos: int,
        end_of_last_block: int,
        next_char_pos: int,
    ) -> list[Block]:
        text: str, code_tokenizer: CodeTokenizer, block_start_pos: int, end_of_last_block: int, next_char_pos: int
    ) -> List[Block]:
        text: str, code_tokenizer: CodeTokenizer, block_start_pos: int, end_of_last_block: int, next_char_pos: int
    ) -> List[Block]:
        """Extract the blocks from the found code.

        If there is text before the current block, create a TextBlock from that.

        If the block is empty, return a TextBlock with the delimiters.

        If the block is not empty, tokenize it and return the result.
        If there is only a variable or value in the code block,
        return just that, instead of the CodeBlock.
        """
        new_blocks: list[Block] = []
        new_blocks: list[Block] = []
        if block_start_pos > end_of_last_block:
            new_blocks.append(
                TextBlock.from_text(
                    text,
                    end_of_last_block,
                    block_start_pos,
                )
            )

        content_with_delimiters = text[block_start_pos : next_char_pos + 1]
        content_with_delimiters = text[block_start_pos : next_char_pos + 1]
        content_with_delimiters = text[block_start_pos : next_char_pos + 1]
        content_with_delimiters = text[block_start_pos : next_char_pos + 1]
        content_with_delimiters = text[block_start_pos : next_char_pos + 1]
        content_with_delimiters = text[block_start_pos : next_char_pos + 1]  # noqa: E203
        content_without_delimiters = content_with_delimiters[2:-2].strip()

        if len(content_without_delimiters) == 0:
            # If what is left is empty (only {{}}), consider the raw block
            # a TextBlock
            new_blocks.append(TextBlock.from_text(content_with_delimiters))
            return new_blocks

        try:
            code_blocks = code_tokenizer.tokenize(content_without_delimiters)
        except BlockSyntaxError as e:
        except BlockSyntaxError as e:
        except (
            CodeBlockTokenError,
            CodeBlockSyntaxError,
            VarBlockSyntaxError,
            ValBlockSyntaxError,
            FunctionIdBlockSyntaxError,
        ) as e:
            msg = f"Failed to tokenize code block: {content_without_delimiters}. {e}"
            logger.warning(msg)
            raise TemplateSyntaxError(msg) from e

        if code_blocks[0].type in (
            BlockTypes.VALUE,
            BlockTypes.VARIABLE,
        ):
            new_blocks.append(code_blocks[0])
            return new_blocks
        try:
            new_blocks.append(
                CodeBlock(content=content_without_delimiters, tokens=code_blocks)
            )
            new_blocks.append(
                CodeBlock(content=content_without_delimiters, tokens=code_blocks)
            )
            new_blocks.append(
                CodeBlock(content=content_without_delimiters, tokens=code_blocks)
            )
            new_blocks.append(CodeBlock(content=content_without_delimiters, tokens=code_blocks))
            return new_blocks
        except CodeBlockTokenError as e:
            msg = f"Failed to tokenize code block: {content_without_delimiters}. {e}"
            logger.warning(msg)
            raise TemplateSyntaxError(msg) from e
            # After having found "{{"
            if block_start_found:
                # While inside a text value, when the end quote is found
                if inside_text_value:
                    if current_char == Symbols.ESCAPE_CHAR and self._can_be_escaped(
                        next_char
                    ):
                        skip_next_char = True
                        continue

                    if current_char == text_value_delimiter:
                        inside_text_value = False
                else:
                    # A value starts here
                    if current_char in (Symbols.DBL_QUOTE, Symbols.SGL_QUOTE):
                        inside_text_value = True
                        text_value_delimiter = current_char
                    # If the block ends here
                    elif (
                        current_char == Symbols.BLOCK_ENDER
                        and next_char == Symbols.BLOCK_ENDER
                    ):
                        # If there is plain text between the current
                        # var/val/code block and the previous one,
                        # add it as a text block
                        if block_start_pos > end_of_last_block:
                            blocks.append(
                                TextBlock(
                                    text,
                                    end_of_last_block,
                                    block_start_pos,
                                    log=self.log,
                                )
                            )

                        # Extract raw block
                        content_with_delimiters = text[block_start_pos : cursor + 1]
                        # Remove "{{" and "}}" delimiters and trim whitespace
                        content_without_delimiters = content_with_delimiters[
                            2:-2
                        ].strip()

                        if len(content_without_delimiters) == 0:
                            # If what is left is empty, consider the raw block
                            # a TextBlock
                            blocks.append(
                                TextBlock(content_with_delimiters, log=self.log)
                            )
                        else:
                            code_blocks = self.code_tokenizer.tokenize(
                                content_without_delimiters
                            )

                            first_block_type = code_blocks[0].type

                            if first_block_type == BlockTypes.VARIABLE:
                                if len(code_blocks) > 1:
                                    raise ValueError(
                                        "Invalid token detected after the "
                                        f"variable: {content_without_delimiters}"
                                    )

                                blocks.append(code_blocks[0])
                            elif first_block_type == BlockTypes.VALUE:
                                if len(code_blocks) > 1:
                                    raise ValueError(
                                        "Invalid token detected after the "
                                        "value: {content_without_delimiters}"
                                    )

                                blocks.append(code_blocks[0])
                            elif first_block_type == BlockTypes.FUNCTION_ID:
                                if len(code_blocks) > 2:
                                    raise ValueError(
                                        "Functions support only one "
                                        f"parameter: {content_without_delimiters}"
                                    )

                                blocks.append(
                                    CodeBlock(
                                        content_without_delimiters,
                                        code_blocks,
                                        self.log,
                                    )
                                )
                            else:
                                raise ValueError(
                                    "Code tokenizer returned an incorrect "
                                    f"first token type {first_block_type}"
                                )

                        end_of_last_block = cursor + 1
                        block_start_found = False

        # If there is something left after the last block, capture it as a TextBlock
        if end_of_last_block < len(text):
            blocks.append(TextBlock(text, end_of_last_block, len(text), log=self.log))

        return blocks

    def _can_be_escaped(self, c: str) -> bool:
        return c in (
            Symbols.DBL_QUOTE,
            Symbols.SGL_QUOTE,
            Symbols.ESCAPE_CHAR,
        )
