#!/usr/bin/env python3
"""
Test module for block

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from pydantic import ValidationError
from pytest import raises

from semantic_kernel.template_engine.blocks.block import Block


def test_init():
    block = Block(content="test content")
    assert block.content == "test content"


def test_content_strip():
    block = Block(content=" test content ")
    assert block.content == "test content"


def test_no_content():
    with raises(ValidationError):
        Block()
from logging import Logger

from pytest import raises

from semantic_kernel.template_engine.blocks.block import Block
from semantic_kernel.template_engine.blocks.block_types import BlockTypes
from semantic_kernel.utils.null_logger import NullLogger


def test_init():
    block = Block(content="test content", log=NullLogger())
    assert block.content == "test content"
    assert isinstance(block.log, Logger)


def test_type_property():
    block = Block()
    assert block.type == BlockTypes.UNDEFINED


def test_is_valid_not_implemented():
    block = Block()
    with raises(NotImplementedError):
        block.is_valid()
