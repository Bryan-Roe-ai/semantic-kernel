# Copyright (c) Microsoft. All rights reserved.

import logging
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream

from semantic_kernel.exceptions import CodeBlockSyntaxError
from semantic_kernel.template_engine.blocks.block import Block
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< main

from semantic_kernel.exceptions import CodeBlockSyntaxError
=======
<<<<<<< div
=======
>>>>>>> main
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
<<<<<<< main

from semantic_kernel.exceptions import CodeBlockSyntaxError
=======
from typing import List

>>>>>>> ms/small_fixes
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
>>>>>>> origin/main
from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.template_engine.blocks.block_errors import CodeBlockSyntaxError
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.template_engine.blocks.block_errors import CodeBlockSyntaxError
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> origin/main
from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.template_engine.blocks.block_errors import CodeBlockSyntaxError
>>>>>>> Stashed changes
=======
>>>>>>> origin/main
from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.template_engine.blocks.block_errors import CodeBlockSyntaxError
>>>>>>> Stashed changes
>>>>>>> head
from semantic_kernel.template_engine.blocks.block_types import BlockTypes
from semantic_kernel.template_engine.blocks.function_id_block import FunctionIdBlock
from semantic_kernel.template_engine.blocks.named_arg_block import NamedArgBlock
from semantic_kernel.template_engine.blocks.symbols import Symbols
from semantic_kernel.template_engine.blocks.val_block import ValBlock
from semantic_kernel.template_engine.blocks.var_block import VarBlock

logger: logging.Logger = logging.getLogger(__name__)


# BNF parsed by CodeTokenizer:
# [template]       ::= "" | [variable] " " [template]
#                         | [value] " " [template]
#                         | [function-call] " " [template]
# [variable]       ::= "$" [valid-name]
# [value]          ::= "'" [text] "'" | '"' [text] '"'
# [function-call]  ::= [function-id] | [function-id] [parameter]
# [parameter]      ::= [variable] | [value]
class CodeTokenizer:
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< main
=======
<<<<<<< main
>>>>>>> origin/main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< main
<<<<<<< div
>>>>>>> main
=======
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> origin/main
>>>>>>> head
    """Tokenize the code text into blocks."""

    @staticmethod
    def tokenize(text: str) -> list[Block]:
        """Tokenize the code text into blocks."""
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< main
=======
=======
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
>>>>>>> head
=======
    @staticmethod
    def tokenize(text: str) -> List[Block]:
>>>>>>> ms/small_fixes
<<<<<<< div
<<<<<<< div
=======
<<<<<<< head
>>>>>>> head
>>>>>>> origin/main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< div
>>>>>>> main
=======
=======
<<<<<<< main
=======
=======
    @staticmethod
    def tokenize(text: str) -> List[Block]:
>>>>>>> ms/small_fixes
>>>>>>> Stashed changes
=======
<<<<<<< main
=======
=======
    @staticmethod
    def tokenize(text: str) -> List[Block]:
>>>>>>> ms/small_fixes
>>>>>>> Stashed changes
>>>>>>> origin/main
>>>>>>> head
        # Remove spaces, which are ignored anyway
        text = text.strip() if text else ""
        # Render None/empty to []
        if not text:
            return []
        # 1 char only edge case, var and val blocks are invalid with one char, so it must be a function id block
        if len(text) == 1:
            return [FunctionIdBlock(content=text)]

        # Track what type of token we're reading
        current_token_type = None

        # Track the content of the current token
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        current_token_content: list[str] = []
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< main
        current_token_content: list[str] = []
=======
=======
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
<<<<<<< main
        current_token_content: list[str] = []
=======
>>>>>>> Stashed changes
=======
<<<<<<< main
        current_token_content: list[str] = []
=======
>>>>>>> Stashed changes
>>>>>>> head
<<<<<<< main
        current_token_content: list[str] = []
=======
        current_token_content: List[str] = []
>>>>>>> ms/small_fixes
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
>>>>>>> origin/main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< div
>>>>>>> main
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> origin/main
>>>>>>> head

        # Other state we need to track
        text_value_delimiter = None
        space_separator_found = False
        skip_next_char = False
        next_char = ""
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        blocks: list[Block] = []
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< main
        blocks: list[Block] = []
=======
=======
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
<<<<<<< main
        blocks: list[Block] = []
=======
>>>>>>> Stashed changes
=======
<<<<<<< main
        blocks: list[Block] = []
=======
>>>>>>> Stashed changes
>>>>>>> head
<<<<<<< main
        blocks: list[Block] = []
=======
        blocks: List[Block] = []
>>>>>>> ms/small_fixes
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
>>>>>>> origin/main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< div
>>>>>>> main
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> origin/main
>>>>>>> head

        for index, current_char in enumerate(text[:-1]):
            next_char = text[index + 1]

            if skip_next_char:
                skip_next_char = False
                continue

            # First char is easy
            if index == 0:
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
                # If the current char is escaping the next special char we:
                #  - skip the current char (escape char)
                #  - add the next char (special char)
                #  - jump to the one after (to handle "\\" properly)
                if current_char == Symbols.ESCAPE_CHAR and next_char in (
                    Symbols.DBL_QUOTE,
                    Symbols.SGL_QUOTE,
                    Symbols.ESCAPE_CHAR,
                ):
                    current_token_content.append(next_char)
                    skip_next_char = True
                    continue

                current_token_content.append(current_char)

                # When we reach the end of the value, we add the block
                if current_char == text_value_delimiter:
                    blocks.append(ValBlock(content="".join(current_token_content)))
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
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< main
=======
<<<<<<< main
>>>>>>> origin/main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< main
<<<<<<< div
>>>>>>> main
=======
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> origin/main
>>>>>>> head
                        blocks.append(
                            NamedArgBlock(content="".join(current_token_content))
                        )
                    else:
                        blocks.append(
                            FunctionIdBlock(content="".join(current_token_content))
                        )
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< main
=======
<<<<<<< div
=======
>>>>>>> main
=======
>>>>>>> head
=======
>>>>>>> origin/main
=======
=======
<<<<<<< main
=======
=======
>>>>>>> Stashed changes
=======
<<<<<<< main
=======
=======
>>>>>>> Stashed changes
                        blocks.append(NamedArgBlock(content="".join(current_token_content)))
                    else:
                        blocks.append(FunctionIdBlock(content="".join(current_token_content)))
>>>>>>> ms/small_fixes
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
>>>>>>> origin/main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< div
>>>>>>> main
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> origin/main
>>>>>>> head
                    current_token_content.clear()

                space_separator_found = True
                current_token_type = None

                continue

            # If we're not inside a quoted value, and we're not processing a space
            current_token_content.append(current_char)

            if current_token_type is None:
                if not space_separator_found:
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
                    raise CodeBlockSyntaxError(
                        "Tokens must be separated by one space least"
                    )
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< main
                    raise CodeBlockSyntaxError(
                        "Tokens must be separated by one space least"
                    )
=======
<<<<<<< div
=======
>>>>>>> main
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
<<<<<<< main
                    raise CodeBlockSyntaxError(
                        "Tokens must be separated by one space least"
                    )
=======
                    raise CodeBlockSyntaxError("Tokens must be separated by one space least")
>>>>>>> ms/small_fixes
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
>>>>>>> origin/main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< div
>>>>>>> main
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> origin/main
>>>>>>> head

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
