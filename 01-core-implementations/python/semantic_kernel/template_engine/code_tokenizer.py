# Copyright (c) Microsoft. All rights reserved.

import logging

from semantic_kernel.exceptions import CodeBlockSyntaxError
from semantic_kernel.template_engine.blocks.block import Block

from semantic_kernel.exceptions import CodeBlockSyntaxError

from semantic_kernel.exceptions import CodeBlockSyntaxError
from typing import List

from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.template_engine.blocks.block_errors import CodeBlockSyntaxError
from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.template_engine.blocks.block_errors import CodeBlockSyntaxError
from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.template_engine.blocks.block_errors import CodeBlockSyntaxError
from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.template_engine.blocks.block_errors import CodeBlockSyntaxError
from semantic_kernel.template_engine.blocks.block_types import BlockTypes
from semantic_kernel.template_engine.blocks.function_id_block import FunctionIdBlock
from semantic_kernel.template_engine.blocks.named_arg_block import NamedArgBlock
from semantic_kernel.template_engine.blocks.symbols import Symbols
from semantic_kernel.template_engine.blocks.val_block import ValBlock
from semantic_kernel.template_engine.blocks.var_block import VarBlock

logger: logging.Logger = logging.getLogger(__name__)
from logging import Logger
from typing import List

from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.template_engine.blocks.block_types import BlockTypes
from semantic_kernel.template_engine.blocks.function_id_block import FunctionIdBlock
from semantic_kernel.template_engine.blocks.symbols import Symbols
from semantic_kernel.template_engine.blocks.val_block import ValBlock
from semantic_kernel.template_engine.blocks.var_block import VarBlock
from semantic_kernel.utils.null_logger import NullLogger


# BNF parsed by CodeTokenizer:
# [template]       ::= "" | [variable] " " [template]
#                         | [value] " " [template]
#                         | [function-call] " " [template]
# [variable]       ::= "$" [valid-name]
# [value]          ::= "'" [text] "'" | '"' [text] '"'
# [function-call]  ::= [function-id] | [function-id] [parameter]
# [parameter]      ::= [variable] | [value]
class CodeTokenizer:
    """Tokenize the code text into blocks."""

    @staticmethod
    def tokenize(text: str) -> list[Block]:
        """Tokenize the code text into blocks."""
    @staticmethod
    def tokenize(text: str) -> List[Block]:
    @staticmethod
    def tokenize(text: str) -> List[Block]:
    @staticmethod
    def tokenize(text: str) -> List[Block]:
        # Remove spaces, which are ignored anyway
        text = text.strip() if text else ""
        # Render None/empty to []
        if not text:
            return []
        # 1 char only edge case, var and val blocks are invalid with one char, so it must be a function id block
        if len(text) == 1:
            return [FunctionIdBlock(content=text)]
    def __init__(self, log: Logger = None):
        self.log = log or NullLogger()

    def tokenize(self, text: str) -> List[Block]:
        # Remove spaces, which are ignored anyway
        text = text.strip() if text else ""

        # Render None/empty to []
        if not text or text == "":
            return []

        # Track what type of token we're reading
        current_token_type = None

        # Track the content of the current token
        current_token_content: list[str] = []
        current_token_content: list[str] = []

        # Other state we need to track
        text_value_delimiter = None
        space_separator_found = False
        skip_next_char = False
        next_char = ""
        blocks: list[Block] = []

        for index, current_char in enumerate(text[:-1]):
            next_char = text[index + 1]
        current_token_content = []

        # Other state we need to track
        text_value_delimiter = None
        blocks = []
        next_char = text[0]
        space_separator_found = False
        skip_next_char = False

        # 1 char only edge case
        if len(text) == 1:
            if next_char == Symbols.VAR_PREFIX:
                blocks.append(VarBlock(text, self.log))
            elif next_char in (Symbols.DBL_QUOTE, Symbols.SGL_QUOTE):
                blocks.append(ValBlock(text, self.log))
            else:
                blocks.append(FunctionIdBlock(text, self.log))

            return blocks

        for next_char_cursor in range(1, len(text)):
            current_char = next_char
            next_char = text[next_char_cursor]

            if skip_next_char:
                skip_next_char = False
                continue

            # First char is easy
            if index == 0:
            if next_char_cursor == 1:
                if current_char == Symbols.VAR_PREFIX:
                    current_token_type = BlockTypes.VARIABLE
                elif current_char in (Symbols.DBL_QUOTE, Symbols.SGL_QUOTE):
                    current_token_type = BlockTypes.VALUE
                    text_value_delimiter = current_char
                else:
                    current_token_type = BlockTypes.FUNCTION_ID

                current_token_content.append(current_char)
                continue

            # While reading values between quotes
            if current_token_type in (BlockTypes.VALUE, BlockTypes.NAMED_ARG):
            if current_token_type == BlockTypes.VALUE:
                # If the current char is escaping the next special char we:
                #  - skip the current char (escape char)
                #  - add the next char (special char)
                #  - jump to the one after (to handle "\\" properly)
                if current_char == Symbols.ESCAPE_CHAR and next_char in (
                    Symbols.DBL_QUOTE,
                    Symbols.SGL_QUOTE,
                    Symbols.ESCAPE_CHAR,
                if current_char == Symbols.ESCAPE_CHAR and self._can_be_escaped(
                    next_char
                ):
                    current_token_content.append(next_char)
                    skip_next_char = True
                    continue

                current_token_content.append(current_char)

                # When we reach the end of the value, we add the block
                if current_char == text_value_delimiter:
                    blocks.append(ValBlock(content="".join(current_token_content)))
                    blocks.append(ValBlock("".join(current_token_content), self.log))
                    current_token_content.clear()
                    current_token_type = None
                    space_separator_found = False

                continue

            # If we're not between quotes, a space signals the end of the current token
            # Note: there might be multiple consecutive spaces
            if current_char in (
                Symbols.SPACE,
                Symbols.NEW_LINE,
                Symbols.CARRIAGE_RETURN,
                Symbols.TAB,
            ):
                if current_token_type == BlockTypes.VARIABLE:
                    blocks.append(VarBlock(content="".join(current_token_content)))
                    current_token_content.clear()
                elif current_token_type == BlockTypes.FUNCTION_ID:
                    if Symbols.NAMED_ARG_BLOCK_SEPARATOR.value in current_token_content:
                        blocks.append(
                            NamedArgBlock(content="".join(current_token_content))
                        )
                    else:
                        blocks.append(
                            FunctionIdBlock(content="".join(current_token_content))
                        )
                        blocks.append(NamedArgBlock(content="".join(current_token_content)))
                    else:
                        blocks.append(FunctionIdBlock(content="".join(current_token_content)))
            if self._is_blank_space(current_char):
                if current_token_type == BlockTypes.VARIABLE:
                    blocks.append(VarBlock("".join(current_token_content), self.log))
                    current_token_content.clear()
                elif current_token_type == BlockTypes.FUNCTION_ID:
                    blocks.append(
                        FunctionIdBlock("".join(current_token_content), self.log)
                    )
                    current_token_content.clear()

                space_separator_found = True
                current_token_type = None

                continue

            # If we're not inside a quoted value, and we're not processing a space
            # If we're not inside a quoted value and we're not processing a space
            current_token_content.append(current_char)

            if current_token_type is None:
                if not space_separator_found:
                    raise CodeBlockSyntaxError(
                        "Tokens must be separated by one space least"
                    )

                    raise CodeBlockSyntaxError(
                        "Tokens must be separated by one space least"
                    )

                    raise CodeBlockSyntaxError(
                        "Tokens must be separated by one space least"
                    )
                    raise CodeBlockSyntaxError("Tokens must be separated by one space least")

                    raise ValueError("Tokens must be separated by one space least")


                if current_char in (Symbols.DBL_QUOTE, Symbols.SGL_QUOTE):
                    # A quoted value starts here
                    current_token_type = BlockTypes.VALUE
                    text_value_delimiter = current_char
                elif current_char == Symbols.VAR_PREFIX:
                    # A variable starts here
                    current_token_type = BlockTypes.VARIABLE
                else:
                    # A function id starts here
                    current_token_type = BlockTypes.FUNCTION_ID

        # end of main for loop

        # Capture last token
        current_token_content.append(next_char)

        if current_token_type == BlockTypes.VALUE:
            blocks.append(ValBlock(content="".join(current_token_content)))
        elif current_token_type == BlockTypes.VARIABLE:
            blocks.append(VarBlock(content="".join(current_token_content)))
        elif current_token_type == BlockTypes.FUNCTION_ID:
            if Symbols.NAMED_ARG_BLOCK_SEPARATOR.value in current_token_content:
                blocks.append(NamedArgBlock(content="".join(current_token_content)))
            else:
                blocks.append(FunctionIdBlock(content="".join(current_token_content)))
        else:
            raise CodeBlockSyntaxError("Tokens must be separated by one space least")

        return blocks
            blocks.append(ValBlock("".join(current_token_content), self.log))
        elif current_token_type == BlockTypes.VARIABLE:
            blocks.append(VarBlock("".join(current_token_content), self.log))
        elif current_token_type == BlockTypes.FUNCTION_ID:
            blocks.append(FunctionIdBlock("".join(current_token_content), self.log))
        else:
            raise ValueError("Tokens must be separated by one space least")

        return blocks

    def _is_blank_space(self, c: str) -> bool:
        return c in (
            Symbols.SPACE,
            Symbols.NEW_LINE,
            Symbols.CARRIAGE_RETURN,
            Symbols.TAB,
        )

    def _can_be_escaped(self, c: str) -> bool:
        return c in (
            Symbols.DBL_QUOTE,
            Symbols.SGL_QUOTE,
            Symbols.ESCAPE_CHAR,
        )
