#!/usr/bin/env python3
"""
import asyncio
Test module for code block

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from pytest import mark, raises

from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.functions.kernel_function import KernelFunction
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.functions.kernel_function_from_method import (
    KernelFunctionFromMethod,
)
from semantic_kernel.functions.kernel_parameter_metadata import KernelParameterMetadata
from semantic_kernel.functions.kernel_plugin import KernelPlugin
from semantic_kernel.functions.kernel_plugin_collection import (
    KernelPluginCollection,
)
from semantic_kernel.kernel import Kernel
from semantic_kernel.template_engine.blocks.block_errors import (
    CodeBlockRenderException,
    CodeBlockSyntaxError,
    CodeBlockTokenError,
    FunctionIdBlockSyntaxError,
    NamedArgBlockSyntaxError,
    ValBlockSyntaxError,
    VarBlockSyntaxError,
)
from logging import Logger
from unittest.mock import Mock

from pytest import mark, raises

from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.functions.kernel_function import KernelFunction
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.functions.kernel_function_from_method import (
    KernelFunctionFromMethod,
)
from semantic_kernel.functions.kernel_parameter_metadata import KernelParameterMetadata
from semantic_kernel.functions.kernel_plugin import KernelPlugin
from semantic_kernel.functions.kernel_plugin_collection import (
    KernelPluginCollection,
)
from semantic_kernel.kernel import Kernel
from semantic_kernel.memory.null_memory import NullMemory
from semantic_kernel.orchestration.context_variables import ContextVariables
from semantic_kernel.orchestration.delegate_types import DelegateTypes
from semantic_kernel.orchestration.sk_context import SKContext
from semantic_kernel.orchestration.sk_function import SKFunction
from semantic_kernel.skill_definition.read_only_skill_collection_base import (
    ReadOnlySkillCollectionBase,
)
from semantic_kernel.template_engine.blocks.block_errors import (
    CodeBlockRenderError,
    CodeBlockSyntaxError,
    CodeBlockTokenError,
    FunctionIdBlockSyntaxError,
    NamedArgBlockSyntaxError,
    ValBlockSyntaxError,
    VarBlockSyntaxError,
)
from semantic_kernel.template_engine.blocks.block_types import BlockTypes
from semantic_kernel.template_engine.blocks.code_block import CodeBlock
from semantic_kernel.template_engine.blocks.function_id_block import FunctionIdBlock
from semantic_kernel.template_engine.blocks.named_arg_block import NamedArgBlock
from semantic_kernel.template_engine.blocks.val_block import ValBlock
from semantic_kernel.template_engine.blocks.var_block import VarBlock


def test_init():
    target = CodeBlock(
        content="plugin.function 'value'  arg1=$arg1",
    )
    assert len(target.tokens) == 3
    assert target.tokens[0] == FunctionIdBlock(content="plugin.function")
    assert target.tokens[1] == ValBlock(content="'value'")
    assert target.tokens[2] == NamedArgBlock(content="arg1=$arg1")
    assert target.type == BlockTypes.CODE


class TestCodeBlockRendering:
    @mark.asyncio
    async def test_it_throws_if_a_plugins_are_empty(self, kernel: Kernel):


class TestCodeBlockRendering:
    @mark.asyncio
    async def test_it_throws_if_a_plugins_are_empty(self, kernel: Kernel):


class TestCodeBlockRendering:
    def setup_method(self):
        self.kernel = Kernel()

    @mark.asyncio
    async def test_it_throws_if_a_plugins_are_empty(self):
        target = CodeBlock(
            content="functionName",
        )
        assert target.tokens[0].type == BlockTypes.FUNCTION_ID
        with raises(CodeBlockRenderError, match="Plugin collection not set in kernel"):
            await target.render_code(self.kernel, KernelArguments())

    @mark.asyncio
    async def test_it_throws_if_a_plugins_are_empty(self):
        target = CodeBlock(
            content="functionName",
        )
        assert target.tokens[0].type == BlockTypes.FUNCTION_ID
        with raises(CodeBlockRenderError, match="Plugin collection not set in kernel"):
            await target.render_code(self.kernel, KernelArguments())

class TestCodeBlockRendering:
    @mark.asyncio
    async def test_it_throws_if_a_plugins_are_empty(self, kernel: Kernel):tp
    async def test_it_throws_if_a_function_doesnt_exist(self):
        target = CodeBlock(
            content="functionName",
        )
        assert target.tokens[0].type == BlockTypes.FUNCTION_ID
        with raises(
            CodeBlockRenderException, match="Function `functionName` not found"
        ):
            await target.render_code(kernel, KernelArguments())

    async def test_it_throws_if_a_function_doesnt_exist(self, kernel: Kernel):
        target = CodeBlock(
            content="functionName",
        )
        assert target.tokens[0].type == BlockTypes.FUNCTION_ID
        kernel.add_plugin(KernelPlugin(name="test", functions=[]))
        with raises(
            CodeBlockRenderException, match="Function `functionName` not found"
        ):
            await target.render_code(kernel, KernelArguments())

    async def test_it_throws_if_a_function_call_throws(self, kernel: Kernel):
        @kernel_function(name="funcName")
        def invoke():
            raise Exception("function exception")

        function = KernelFunctionFromMethod(
            method=invoke,
            plugin_name="pluginName",
        )

        kernel.add_function(plugin_name="test", function=function)

        target = CodeBlock(
            content="test.funcName",
        )

        with raises(CodeBlockRenderException, match="test.funcName"):
            await target.render_code(kernel, KernelArguments())

    @mark.asyncio
    async def test_it_renders_code_block_consisting_of_just_a_var_block1(
        self, kernel: Kernel
    ):
    async def test_it_renders_code_block_consisting_of_just_a_var_block1(self, kernel: Kernel):
        code_block = CodeBlock(
            content="$var",
        )
        result = await code_block.render_code(kernel, KernelArguments(var="foo"))


    @mark.asyncio
    async def test_it_throws_if_a_function_doesnt_exist(self, kernel: Kernel):
        self.kernel.plugins = KernelPluginCollection()
        dkp = KernelPlugin(name="test", functions=[])
        self.kernel.plugins.add(dkp)
        with raises(CodeBlockRenderError, match="Function `functionName` not found"):
            await target.render_code(self.kernel, KernelArguments())

    @mark.asyncio
    async def test_it_throws_if_a_function_call_throws(self):
        def invoke():
            raise Exception("error")

        function = KernelFunction(
            function_name="funcName",
            plugin_name="pluginName",
            description="",
            function=invoke,
            parameters=[],
            return_parameter=None,
            is_prompt=False,
        )

        dkp = KernelPlugin(name="test", functions=[function])
        plugins = KernelPluginCollection()
        plugins.add(dkp)
        kernel = Kernel()
        kernel.plugins = plugins


    @mark.asyncio
    async def test_it_throws_if_a_function_doesnt_exist(self, kernel: Kernel):
        self.kernel.plugins = KernelPluginCollection()
        dkp = KernelPlugin(name="test", functions=[])
        self.kernel.plugins.add(dkp)
        with raises(CodeBlockRenderError, match="Function `functionName` not found"):
            await target.render_code(self.kernel, KernelArguments())

    @mark.asyncio
    async def test_it_throws_if_a_function_call_throws(self):
        def invoke():
            raise Exception("error")

        function = KernelFunction(
            function_name="funcName",
            plugin_name="pluginName",
            description="",
            function=invoke,
            parameters=[],
            return_parameter=None,
            is_prompt=False,
        )

        dkp = KernelPlugin(name="test", functions=[function])
        plugins = KernelPluginCollection()
        plugins.add(dkp)
        kernel = Kernel()
        kernel.plugins = plugins

        target = CodeBlock(
            content="functionName",
        )
        assert target.tokens[0].type == BlockTypes.FUNCTION_ID
        kernel.add_plugin(KernelPlugin(name="test", functions=[]))
        with raises(
            CodeBlockRenderException, match="Function `functionName` not found"
        ):
            await target.render_code(kernel, KernelArguments())

    @mark.asyncio
    async def test_it_throws_if_a_function_call_throws(self, kernel: Kernel):
        @kernel_function(name="funcName")
        def invoke():
            raise Exception("function exception")

        function = KernelFunctionFromMethod(
            method=invoke,
            plugin_name="pluginName",
        )

        kernel.add_function(plugin_name="test", function=function)

        target = CodeBlock(
            content="test.funcName",
        )

        with raises(CodeBlockRenderException, match="test.funcName"):
            await target.render_code(kernel, KernelArguments())

    @mark.asyncio
    async def test_it_renders_code_block_consisting_of_just_a_var_block1(
        self, kernel: Kernel
    ):
        code_block = CodeBlock(
            content="$var",
        )
        result = await code_block.render_code(kernel, KernelArguments(var="foo"))
        with raises(CodeBlockRenderError):
            await target.render_code(kernel, KernelArguments())

    @mark.asyncio
    async def test_it_renders_code_block_consisting_of_just_a_var_block1(self):
        code_block = CodeBlock(
            content="$var",
        )
        result = await code_block.render_code(self.kernel, KernelArguments(var="foo"))

        assert result == "foo"

    @mark.asyncio
    async def test_it_renders_code_block_consisting_of_just_a_val_block1(
        self, kernel: Kernel
    ):
    async def test_it_renders_code_block_consisting_of_just_a_val_block1(self, kernel: Kernel):
        code_block = CodeBlock(
            content="'ciao'",
        )
        result = await code_block.render_code(kernel, KernelArguments())
        u

    async def test_it_renders_code_block_consisting_of_just_a_val_block1(self):
        code_block = CodeBlock(
            content="'ciao'",
        )
        result = await code_block.render_code(self.kernel, KernelArguments())

        assert result == "ciao"

    @mark.asyncio
    async def test_it_invokes_function_cloning_all_variables(self, kernel: Kernel):
    async def test_it_invokes_function_cloning_all_variables(self):
        # Set up initial context variables
        arguments = KernelArguments(input="zero", var1="uno", var2="due")

        # Create a FunctionIdBlock with the function name
        func_id = FunctionIdBlock(content="test.funcName")
class TestCodeBlock:
    def setup_method(self):
        self.skills = Mock(spec=ReadOnlySkillCollectionBase)
        self.log = Mock(spec=Logger)

    @mark.asyncio
    async def test_it_throws_if_a_function_doesnt_exist(self):
        context = SKContext(
            ContextVariables(),
            memory=NullMemory(),
            skill_collection=self.skills,
            logger=self.log,
        )
        # Make it so our self.skills mock's `has_function` method returns False
        self.skills.has_function.return_value = False
        target = CodeBlock(content="functionName", log=self.log)

        with raises(ValueError):
            await target.render_code_async(context)

    @mark.asyncio
    async def test_it_throws_if_a_function_call_throws(self):
        context = SKContext(
            ContextVariables(),
            memory=NullMemory(),
            skill_collection=self.skills,
            logger=self.log,
        )

        def invoke(_):
            raise Exception("error")

        function = SKFunction(
            delegate_type=DelegateTypes.InSKContext,
            delegate_function=invoke,
            skill_name="",
            function_name="funcName",
            description="",
            parameters=[],
            is_semantic=False,
        )

        self.skills.has_function.return_value = True
        self.skills.get_function.return_value = function

        target = CodeBlock(content="functionName", log=self.log)

        with raises(ValueError):
            await target.render_code_async(context)

    def test_it_has_the_correct_type(self):
        assert CodeBlock(content="", log=self.log).type == BlockTypes.CODE

    def test_it_trims_spaces(self):
        assert CodeBlock(content="  aa  ", log=self.log).content == "aa"

    def test_it_checks_validity_of_internal_blocks(self):
        valid_block1 = FunctionIdBlock(content="x")

        valid_block2 = ValBlock(content="''")
        invalid_block = VarBlock(content="!notvalid")

        code_block1 = CodeBlock(
            tokens=[valid_block1, valid_block2], content="", log=self.log
        )
        code_block2 = CodeBlock(
            tokens=[valid_block1, invalid_block], content="", log=self.log
        )

        is_valid1, _ = code_block1.is_valid()
        is_valid2, _ = code_block2.is_valid()

        assert is_valid1
        assert not is_valid2

    def test_it_requires_a_valid_function_call(self):
        func_id = FunctionIdBlock(content="funcName")

        val_block = ValBlock(content="'value'")
        var_block = VarBlock(content="$var")

        code_block1 = CodeBlock(tokens=[func_id, val_block], content="", log=self.log)
        code_block2 = CodeBlock(tokens=[func_id, var_block], content="", log=self.log)
        code_block3 = CodeBlock(tokens=[func_id, func_id], content="", log=self.log)
        code_block4 = CodeBlock(
            tokens=[func_id, var_block, var_block], content="", log=self.log
        )

        is_valid1, _ = code_block1.is_valid()
        is_valid2, _ = code_block2.is_valid()

        is_valid3, _ = code_block3.is_valid()
        is_valid4, _ = code_block4.is_valid()

        assert is_valid1
        assert is_valid2

        assert not is_valid3
        assert not is_valid4

    @mark.asyncio
    async def test_it_renders_code_block_consisting_of_just_a_var_block1(self):
        variables = ContextVariables()
        variables["varName"] = "foo"

        context = SKContext(
            variables, memory=NullMemory(), skill_collection=None, logger=self.log
        )

        code_block = CodeBlock(content="$varName", log=self.log)
        result = await code_block.render_code_async(context)

        assert result == "foo"

    @mark.asyncio
    async def test_it_renders_code_block_consisting_of_just_a_var_block2(self):
        variables = ContextVariables()
        variables["varName"] = "bar"

        context = SKContext(
            variables, memory=NullMemory(), skill_collection=None, logger=self.log
        )

        code_block = CodeBlock(
            tokens=[VarBlock(content="$varName")], content="", log=self.log
        )
        result = await code_block.render_code_async(context)

        assert result == "bar"

    @mark.asyncio
    async def test_it_renders_code_block_consisting_of_just_a_val_block1(self):
        context = SKContext(
            ContextVariables(),
            memory=NullMemory(),
            skill_collection=None,
            logger=self.log,
        )

        code_block = CodeBlock(content="'ciao'", log=self.log)
        result = await code_block.render_code_async(context)

        assert result == "ciao"

    @mark.asyncio
    async def test_it_renders_code_block_consisting_of_just_a_val_block2(self):
        context = SKContext(
            ContextVariables(),
            memory=NullMemory(),
            skill_collection=None,
            logger=self.log,
        )

        code_block = CodeBlock(
            tokens=[ValBlock(content="'arrivederci'")], content="", log=self.log
        )
        result = await code_block.render_code_async(context)

        assert result == "arrivederci"

    @mark.asyncio
    async def test_it_invokes_function_cloning_all_variables(self):
        # Set up initial context variables
        variables = ContextVariables()
        variables["input"] = "zero"
        variables["var1"] = "uno"
        variables["var2"] = "due"

        # Create a context with the variables, memory, skill collection, and logger
        context = SKContext(
            variables,
            memory=NullMemory(),
            skill_collection=self.skills,
            logger=self.log,
        )

        # Create a FunctionIdBlock with the function name
        func_id = FunctionIdBlock(content="funcName")

        # Set up a canary dictionary to track changes in the context variables
        canary = {"input": "", "var1": "", "var2": ""}

        # Define the function to be invoked, which modifies the canary
        # and context variables
        @kernel_function(name="funcName")
        def invoke(arguments: KernelArguments):
            nonlocal canary
            canary["input"] = arguments["input"]
            canary["var1"] = arguments["var1"]
            canary["var2"] = arguments["var2"]

            arguments["input"] = "overridden"
            arguments["var1"] = "overridden"
            arguments["var2"] = "overridden"

        # Create an KernelFunction with the invoke function as its delegate
        function = KernelFunctionFromMethod(
            method=invoke,
            plugin_name="pluginName",
        )

        kernel.add_plugin(KernelPlugin(name="test", functions=[function]))
        function = KernelFunctionFromMethod(
            method=invoke,
            plugin_name="pluginName",
        )

        kernel.add_plugin(KernelPlugin(name="test", functions=[function]))
        function = KernelFunction(
            function_name="funcName",
            plugin_name="pluginName",
            description="",
            function=invoke,
            parameters=[KernelParameterMetadata(name="arguments", description="", default_value=None, required=True)],
            return_parameter=None,
            is_prompt=False,
        )

        dkp = KernelPlugin(name="test", functions=[function])
        kernel = Kernel()
        kernel.plugins.add(dkp)

        # Create a CodeBlock with the FunctionIdBlock and render it with the context
        code_block = CodeBlock(
            tokens=[func_id],
            content="",
        )
        await code_block.render_code(kernel, arguments)
        def invoke(ctx):
            nonlocal canary
            canary["input"] = ctx["input"]
            canary["var1"] = ctx["var1"]
            canary["var2"] = ctx["var2"]

            ctx["input"] = "overridden"
            ctx["var1"] = "overridden"
            ctx["var2"] = "overridden"

        # Create an SKFunction with the invoke function as its delegate
        function = SKFunction(
            delegate_type=DelegateTypes.InSKContext,
            delegate_function=invoke,
            skill_name="",
            function_name="funcName",
            description="",
            parameters=[],
            is_semantic=False,
        )

        # Mock the skill collection's function retrieval
        self.skills.has_function.return_value = True
        self.skills.get_function.return_value = function

        # Create a CodeBlock with the FunctionIdBlock and render it with the context
        code_block = CodeBlock(tokens=[func_id], content="", log=self.log)
        await code_block.render_code_async(context)

        # Check that the canary values match the original context variables
        assert canary["input"] == "zero"
        assert canary["var1"] == "uno"
        assert canary["var2"] == "due"

        # Check that the original context variables were not modified
        assert arguments["input"] == "zero"
        assert arguments["var1"] == "uno"
        assert arguments["var2"] == "due"

    async def test_it_invokes_function_with_custom_variable(self, kernel: Kernel):
        assert variables["input"] == "zero"
        assert variables["var1"] == "uno"
        assert variables["var2"] == "due"

    @mark.asyncio
    async def test_it_invokes_function_with_custom_variable(self):
        # Define custom variable name and value
        VAR_NAME = "varName"
        VAR_VALUE = "varValue"

        # Set up initial context variables
        arguments = KernelArguments()
        arguments[VAR_NAME] = VAR_VALUE

        # Create a FunctionIdBlock with the function name and a
        # VarBlock with the custom variable
        func_id = FunctionIdBlock(content="test.funcName")
        variables = ContextVariables()
        variables[VAR_NAME] = VAR_VALUE

        # Create a context with the variables, memory, skill collection, and logger
        context = SKContext(
            variables,
            memory=NullMemory(),
            skill_collection=self.skills,
            logger=self.log,
        )

        # Create a FunctionIdBlock with the function name and a
        # VarBlock with the custom variable
        func_id = FunctionIdBlock(content="funcName")
        var_block = VarBlock(content=f"${VAR_NAME}")

        # Set up a canary variable to track changes in the context input
        canary = ""

        # Define the function to be invoked, which modifies the canary variable
        @kernel_function(name="funcName")
        def invoke(arguments: "KernelArguments"):
        @kernel_function(name="funcName")
        def invoke(arguments: "KernelArguments"):
        def invoke(arguments):
            nonlocal canary
            canary = arguments["varName"]
            return arguments["varName"]

        # Create an KernelFunction with the invoke function as its delegate
        function = KernelFunctionFromMethod(
            method=invoke,
            plugin_name="pluginName",
        )

        kernel.add_plugin(KernelPlugin(name="test", functions=[function]))
        function = KernelFunctionFromMethod(
            method=invoke,
            plugin_name="pluginName",
        )

        kernel.add_plugin(KernelPlugin(name="test", functions=[function]))
        function = KernelFunction(
            function=invoke,
            plugin_name="pluginName",
            function_name="funcName",
            description="",
            parameters=[KernelParameterMetadata(name="arguments", description="", default_value=None, required=True)],
            return_parameter=None,
            is_prompt=False,
        )

        dkp = KernelPlugin(name="test", functions=[function])
        kernel = Kernel()
        kernel.plugins.add(dkp)

        # Create a CodeBlock with the FunctionIdBlock and VarBlock,
        # and render it with the context
        code_block = CodeBlock(
            tokens=[func_id, var_block],
            content="",
        )
        result = await code_block.render_code(kernel, arguments)
        def invoke(ctx):
            nonlocal canary
            canary = ctx["input"]

        # Create an SKFunction with the invoke function as its delegate
        function = SKFunction(
            delegate_type=DelegateTypes.InSKContext,
            delegate_function=invoke,
            skill_name="",
            function_name="funcName",
            description="",
            parameters=[],
            is_semantic=False,
        )

        # Mock the skill collection's function retrieval
        self.skills.has_function.return_value = True
        self.skills.get_function.return_value = function

        # Create a CodeBlock with the FunctionIdBlock and VarBlock,
        # and render it with the context
        code_block = CodeBlock(tokens=[func_id, var_block], content="", log=self.log)
        result = await code_block.render_code_async(context)

        # Check that the result matches the custom variable value
        assert result == VAR_VALUE
        # Check that the canary value matches the custom variable value
        assert canary == VAR_VALUE

    async def test_it_invokes_function_with_custom_value(self, kernel: Kernel):
        # Define a value to be used in the test
        VALUE = "value"

        # Create a FunctionIdBlock with the function name and a ValBlock with the value
        func_id = FunctionIdBlock(content="test.funcName")
        val_block = ValBlock(content=f"'{VALUE}'")

        # Set up a canary variable to track changes in the context input
        canary = ""

        # Define the function to be invoked, which modifies the canary variable
        @kernel_function(name="funcName")
        def invoke(arguments):
            nonlocal canary
            canary = arguments["input"]
            return arguments["input"]

        # Create an KernelFunction with the invoke function as its delegate
        function = KernelFunctionFromMethod(
            method=invoke,
            plugin_name="pluginName",
        )

        kernel.add_plugin(KernelPlugin(name="test", functions=[function]))
        function = KernelFunctionFromMethod(
            method=invoke,
            plugin_name="pluginName",
        )

        kernel.add_plugin(KernelPlugin(name="test", functions=[function]))
        function = KernelFunction(
            function=invoke,
            plugin_name="pluginName",
            function_name="funcName",
            description="",
            parameters=[KernelParameterMetadata(name="arguments", description="", default_value=None, required=True)],
            return_parameter=None,
            is_prompt=False,
        )

        dkp = KernelPlugin(name="test", functions=[function])
        kernel = Kernel()
        kernel.plugins.add(dkp)

        # Create a CodeBlock with the FunctionIdBlock and ValBlock,
        # and render it with the context
        code_block = CodeBlock(
            tokens=[func_id, val_block],
            content="",
        )
        result = await code_block.render_code(kernel, KernelArguments(input="value"))

        # Check that the result matches the value
        assert str(result) == VALUE
        # Check that the canary value matches the value
        assert canary == VALUE

    @mark.asyncio
    async def test_it_invokes_function_with_multiple_arguments(self, kernel: Kernel):
        # Define a value to be used in the test
        VALUE = "value"

        code_block = CodeBlock(
            content=" ",
            tokens=[
                FunctionIdBlock(
                    content="test.funcName",
                    plugin_name="test",
                    function_name="funcName",
                    validated=True,
                ),
                FunctionIdBlock(content="test.funcName", plugin_name="test", function_name="funcName", validated=True),
                FunctionIdBlock(content="test.funcName", plugin_name="test", function_name="funcName", validated=True),
                FunctionIdBlock(content="test.funcName", plugin_name="test", function_name="funcName", validated=True),
                ValBlock(content=f'"{VALUE}"'),
                NamedArgBlock(content="arg1=$arg1"),
                NamedArgBlock(content='arg2="arg2"'),
            ],
        )
        # Set up a canary variable to track changes in the context input
        canary = ""

        # Define the function to be invoked, which modifies the canary variable
        @kernel_function(name="funcName")
        def invoke(input, arg1, arg2):
            nonlocal canary
            canary = f"{input} {arg1} {arg2}"
            return input

        # Create an KernelFunction with the invoke function as its delegate
        function = KernelFunctionFromMethod(
            method=invoke,
            plugin_name="pluginName",
        )

        kernel.add_plugin(KernelPlugin(name="test", functions=[function]))
        function = KernelFunction(
            function=invoke,
            plugin_name="pluginName",
            function_name="funcName",
            description="",
            parameters=[
                KernelParameterMetadata(name="input", description="", default_value=None, required=True),
                KernelParameterMetadata(name="arg1", description="", default_value=None, required=True),
                KernelParameterMetadata(name="arg2", description="", default_value=None, required=True),
            ],
            return_parameter=None,
            is_prompt=False,
        )

        dkp = KernelPlugin(name="test", functions=[function])
        kernel = Kernel()
        kernel.plugins.add(dkp)

        # Create a CodeBlock with the FunctionIdBlock and ValBlock,
        # and render it with the context
        result = await code_block.render_code(kernel, KernelArguments(arg1="arg1"))

        # Check that the result matches the value
        assert str(result) == VALUE
        # Check that the canary value matches the value
        assert canary == f"{VALUE} arg1 arg2"

    @mark.asyncio
    async def test_it_invokes_function_with_only_named_arguments(self, kernel: Kernel):
        code_block = CodeBlock(
            content=" ",
            tokens=[
                FunctionIdBlock(
                    content="test.funcName",
                    plugin_name="test",
                    function_name="funcName",
                ),
    async def test_it_invokes_function_with_only_named_arguments(self):
        code_block = CodeBlock(
            content=" ",
            tokens=[
                FunctionIdBlock(content="test.funcName", plugin_name="test", function_name="funcName"),
                NamedArgBlock(content="arg1=$arg1"),
                NamedArgBlock(content='arg2="arg2"'),
            ],
        )
    @mark.asyncio
    async def test_it_invokes_function_with_custom_value(self):
        # Define a value to be used in the test
        VALUE = "value"

        # Create a context with empty variables, memory, skill collection, and logger
        context = SKContext(
            ContextVariables(),
            memory=NullMemory(),
            skill_collection=self.skills,
            logger=self.log,
        )

        # Create a FunctionIdBlock with the function name and a ValBlock with the value
        func_id = FunctionIdBlock(content="funcName")
        val_block = ValBlock(content=f"'{VALUE}'")

        # Set up a canary variable to track changes in the context input
        canary = ""

        # Define the function to be invoked, which modifies the canary variable
        @kernel_function(name="funcName")
        def invoke(arg1, arg2):
            nonlocal canary
            canary = f"{arg1} {arg2}"
            return arg1

        # Create an KernelFunction with the invoke function as its delegate
        function = KernelFunctionFromMethod(
            method=invoke,
            plugin_name="pluginName",
        )

        kernel.add_plugin(KernelPlugin(name="test", functions=[function]))
        function = KernelFunction(
            function=invoke,
            plugin_name="pluginName",
            function_name="funcName",
            description="",
            parameters=[
                KernelParameterMetadata(name="arg1", description="", default_value=None, required=True),
                KernelParameterMetadata(name="arg2", description="", default_value=None, required=True),
            ],
            return_parameter=None,
            is_prompt=False,
        )

        dkp = KernelPlugin(name="test", functions=[function])
        kernel = Kernel()
        kernel.plugins.add(dkp)

        # Create a CodeBlock with the FunctionIdBlock and ValBlock,
        # and render it with the context
        result = await code_block.render_code(kernel, KernelArguments(arg1="arg1"))

        # Check that the result matches the value
        assert str(result) == "arg1"
        # Check that the canary value matches the value
        assert canary == "arg1 arg2"

    @mark.asyncio
    async def test_it_fails_on_function_without_args(self, kernel: Kernel):
        code_block = CodeBlock(
            content=" ",
            tokens=[
                FunctionIdBlock(
                    content="test.funcName",
                    plugin_name="test",
                    function_name="funcName",
                ),
    async def test_it_fails_on_function_without_args(self):
        code_block = CodeBlock(
            content=" ",
            tokens=[
                FunctionIdBlock(content="test.funcName", plugin_name="test", function_name="funcName"),
                NamedArgBlock(content="arg1=$arg1"),
                NamedArgBlock(content='arg2="arg2"'),
            ],
        )

        @kernel_function(name="funcName")
        def invoke():
            return "function without args"

        # Create an KernelFunction with the invoke function as its delegate
        function = KernelFunctionFromMethod(
            method=invoke,
            plugin_name="test",
        )

        kernel.add_plugin(KernelPlugin(name="test", functions=[function]))
        function = KernelFunction(
            function=invoke,
            plugin_name="test",
            function_name="funcName",
            description="",
            parameters=[],
            return_parameter=None,
            is_prompt=False,
        )

        dkp = KernelPlugin(name="test", functions=[function])
        kernel = Kernel()
        kernel.plugins.add(dkp)

        # Create a CodeBlock with the FunctionIdBlock and ValBlock,
        # and render it with the context
        with raises(
            CodeBlockRenderException,
            match="Function test.funcName does not take any arguments \
but it is being called in the template with 2 arguments.",
        ):
            await code_block.render_code(kernel, KernelArguments(arg1="arg1"))


@mark.parametrize(
    "token2",
    [
        "",
        "arg2=$arg!2",
        "arg2='va\"l'",
    ],
    ids=[
        "empty",
        "invalid_named_arg",
        "invalid_named_arg_val",
    ],
)
@mark.parametrize(
    "token1",
    [
        "",
        "$var!",
        "\"val'",
        "arg1=$arg!1",
        "arg1='va\"l'",
    ],
    ids=[
        "empty",
        "invalid_var",
        "invalid_val",
        "invalid_named_arg",
        "invalid_named_arg_val",
    ],
)
@mark.parametrize(
    "token0",
    [
        "plugin.func.test",
        "$var!",
        '"va"l"',
    ],
    ids=[
        "invalid_func",
        "invalid_var",
        "invalid_val",
    ],
)
def test_block_validation(token0, token1, token2):
    with raises((
        FunctionIdBlockSyntaxError,
        VarBlockSyntaxError,
        ValBlockSyntaxError,
        NamedArgBlockSyntaxError,
        CodeBlockSyntaxError,
    )):
        CodeBlock(
            content=f"{token0} {token1} {token2}",
        )


@mark.parametrize(
    "token2, token2valid",
    [
        ("", True),
        ("plugin.func", False),
        ("$var", False),
        ('"val"', False),
        ("arg1=$arg1", True),
        ("arg1='val'", True),
    ],
    ids=[
        "empty",
        "func_invalid",
        "invalid_var",
        "invalid_val",
        "valid_named_arg",
        "valid_named_arg_val",
    ],
)
@mark.parametrize(
    "token1, token1valid",
    [
        ("", True),
        ("plugin.func", False),
        ("$var", True),
        ('"val"', True),
        ("arg1=$arg1", True),
        ("arg1='val'", True),
    ],
    ids=[
        "empty",
        "func_invalid",
        "var",
        "val",
        "valid_named_arg",
        "valid_named_arg_val",
    ],
)
@mark.parametrize(
    "token0, token0valid",
    [
        ("func", True),
        ("plugin.func", True),
        ("$var", True),
        ('"val"', True),
        ("arg1=$arg1", False),
        ("arg1='val'", False),
    ],
    ids=[
        "single_name_func",
        "FQN_func",
        "var",
        "val",
        "invalid_named_arg",
        "invalid_named_arg_val",
    ],
)
def test_positional_validation(
    token0, token0valid, token1, token1valid, token2, token2valid
):
    if not token1 and not token2valid:
        mark.skipif(f"{token0} {token1} {token2}", reason="Not applicable")
        return
    valid = token0valid and token1valid and token2valid
    if token0 in ["$var", '"val"']:
        valid = True
    content = f"{token0} {token1} {token2}"
    if valid:
        target = CodeBlock(
            content=content,
        )
        assert target.content == content.strip()
    else:
        with raises(CodeBlockTokenError):
            CodeBlock(
                content=content,
            )


@mark.parametrize(
    "case, result",
    [
        (r"{$a", False),
    ],
)
def test_edge_cases(case, result):
    if result:
        target = CodeBlock(
            content=case,
        )
        assert target.content == case
    else:
        with raises(FunctionIdBlockSyntaxError):
            CodeBlock(
                content=case,
            )


def test_no_tokens():
    with raises(CodeBlockTokenError):
        CodeBlock(content="", tokens=[])
        def invoke(ctx):
            nonlocal canary
            canary = ctx["input"]

        # Create an SKFunction with the invoke function as its delegate
        function = SKFunction(
            delegate_type=DelegateTypes.InSKContext,
            delegate_function=invoke,
            skill_name="",
            function_name="funcName",
            description="",
            parameters=[],
            is_semantic=False,
        )

        # Mock the skill collection's function retrieval
        self.skills.has_function.return_value = True
        self.skills.get_function.return_value = function

        # Create a CodeBlock with the FunctionIdBlock and ValBlock,
        # and render it with the context
        code_block = CodeBlock(tokens=[func_id, val_block], content="", log=self.log)
        result = await code_block.render_code_async(context)

        # Check that the result matches the value
        assert result == VALUE
        # Check that the canary value matches the value
        assert canary == VALUE
