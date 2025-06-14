# Copyright (c) Microsoft. All rights reserved.


from pytest import mark, raises

from semantic_kernel.exceptions import FunctionIdBlockSyntaxError
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.kernel import Kernel
from semantic_kernel.exceptions import FunctionIdBlockSyntaxError
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.kernel import Kernel
from semantic_kernel.exceptions import FunctionIdBlockSyntaxError
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.kernel import Kernel
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.kernel import Kernel
from semantic_kernel.template_engine.blocks.block_errors import FunctionIdBlockSyntaxError
from logging import Logger

from pytest import mark, raises

from semantic_kernel.orchestration.context_variables import ContextVariables
from semantic_kernel.template_engine.blocks.block_types import BlockTypes
from semantic_kernel.template_engine.blocks.function_id_block import FunctionIdBlock


def test_init():
    function_id_block = FunctionIdBlock(content="plugin.function")
    assert function_id_block.content == "plugin.function"
    assert function_id_block.plugin_name == "plugin"
    assert function_id_block.function_name == "function"
    assert function_id_block.type == BlockTypes.FUNCTION_ID


def test_init_function_only():
    function_id_block = FunctionIdBlock(content="function")
    assert function_id_block.content == "function"
    assert not function_id_block.plugin_name
    assert function_id_block.function_name == "function"
    assert function_id_block.type == BlockTypes.FUNCTION_ID


    function_id_block = FunctionIdBlock(
        content="skill.function", log=Logger("test_logger")
    )
    assert function_id_block.content == "skill.function"
    assert isinstance(function_id_block.log, Logger)


def test_type_property():
    function_id_block = FunctionIdBlock(content="skill.function")
    assert function_id_block.type == BlockTypes.FUNCTION_ID


def test_is_valid():
    function_id_block = FunctionIdBlock(content="skill.function")
    is_valid, error_msg = function_id_block.is_valid()
    assert is_valid
    assert error_msg == ""


def test_is_valid_empty_identifier():
    function_id_block = FunctionIdBlock(content="")
    is_valid, error_msg = function_id_block.is_valid()
    assert not is_valid
    assert error_msg == "The function identifier is empty"


def test_render():
    function_id_block = FunctionIdBlock(content="skill.function")
    rendered_value = function_id_block.render(ContextVariables())
    assert rendered_value == "skill.function"


def test_init_value_error():
    with raises(ValueError):
        FunctionIdBlock(content="skill.nope.function")


def test_it_trims_spaces():
    assert FunctionIdBlock(content="  aa  ").content == "aa"


@mark.parametrize(
    "name",
    [
        "0",
        "1",
        "a",
        "_",
        "01",
        "01a",
        "a01",
        "_0",
        "a01_",
        "_a01",
    ],
)
def test_valid_syntax(name):
    target = FunctionIdBlock(content=name)
    assert target.content == name


@mark.parametrize(
    "content",
    ["", "plugin.nope.function", "func-tion", "plu-in.function", ".function"],
    ids=["empty", "three_parts", "invalid_function", "invalid_plugin", "no_plugin"],
)
def test_syntax_error(content):
    with raises(FunctionIdBlockSyntaxError, match=rf".*{content}.*"):
        FunctionIdBlock(content=content)


def test_render():
    kernel = Kernel()
    function_id_block = FunctionIdBlock(content="plugin.function")
    rendered_value = function_id_block.render(kernel, KernelArguments())
    assert rendered_value == "plugin.function"


def test_render_function_only():
    kernel = Kernel()
    function_id_block = FunctionIdBlock(content="function")
    rendered_value = function_id_block.render(kernel, KernelArguments())
    assert rendered_value == "function"
    "name, is_valid",
    [
        ("0", True),
        ("1", True),
        ("a", True),
        ("_", True),
        ("01", True),
        ("01a", True),
        ("a01", True),
        ("_0", True),
        ("a01_", True),
        ("_a01", True),
        (".", True),
        ("a.b", True),
        ("-", False),
        ("a b", False),
        ("a\nb", False),
        ("a\tb", False),
        ("a\rb", False),
        ("a,b", False),
        ("a-b", False),
        ("a+b", False),
        ("a~b", False),
        ("a`b", False),
        ("a!b", False),
        ("a@b", False),
        ("a#b", False),
        ("a$b", False),
        ("a%b", False),
        ("a^b", False),
        ("a*b", False),
        ("a(b", False),
        ("a)b", False),
        ("a|b", False),
        ("a{b", False),
        ("a}b", False),
        ("a[b", False),
        ("a]b", False),
        ("a:b", False),
        ("a;b", False),
        ("a'b", False),
        ('a"b', False),
        ("a<b", False),
        ("a>b", False),
        ("a/b", False),
        ("a\\b", False),
    ],
)
def test_it_allows_underscore_dots_letters_and_digits(name, is_valid):
    target = FunctionIdBlock(content=f" {name} ")

    valid, _ = target.is_valid()
    assert valid == is_valid


def test_it_allows_only_one_dot():
    target1 = FunctionIdBlock(content="functionName")
    target2 = FunctionIdBlock(content="skillName.functionName")

    with raises(ValueError):
        FunctionIdBlock(content="foo.skillName.functionName")

    assert target1.is_valid() == (True, "")
    assert target2.is_valid() == (True, "")
