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
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> main
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
# Copyright (c) Microsoft. All rights reserved.

from semantic_kernel.connectors.ai.prompt_execution_settings import (
    PromptExecutionSettings,
)
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
<<<<<<< HEAD
=======
=======
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
>>>>>>> f40c1f2075e2443c31c57c34f5f66c2711a8db75
>>>>>>> main
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
from semantic_kernel.functions.kernel_arguments import KernelArguments


def test_kernel_arguments():
    kargs = KernelArguments()
    assert kargs is not None
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    assert kargs.execution_settings is None
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
    assert kargs.execution_settings is None
=======
<<<<<<< HEAD
    assert kargs.execution_settings is None
=======
    assert kargs.execution_settings == {}
>>>>>>> f40c1f2075e2443c31c57c34f5f66c2711a8db75
>>>>>>> main
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
    assert not kargs.keys()


def test_kernel_arguments_with_input():
    kargs = KernelArguments(input=10)
    assert kargs is not None
    assert kargs["input"] == 10


def test_kernel_arguments_with_input_get():
    kargs = KernelArguments(input=10)
    assert kargs is not None
    assert kargs.get("input", None) == 10
    assert not kargs.get("input2", None)


def test_kernel_arguments_keys():
    kargs = KernelArguments(input=10)
    assert kargs is not None
    assert list(kargs.keys()) == ["input"]


def test_kernel_arguments_with_execution_settings():
    test_pes = PromptExecutionSettings(service_id="test")
    kargs = KernelArguments(settings=[test_pes])
    assert kargs is not None
    assert kargs.execution_settings == {"test": test_pes}
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
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> main
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


def test_kernel_arguments_bool():
    # An empty KernelArguments object should return False
    assert not KernelArguments()
    # An KernelArguments object with keyword arguments should return True
    assert KernelArguments(input=10)
    # An KernelArguments object with execution_settings should return True
    assert KernelArguments(settings=PromptExecutionSettings(service_id="test"))
    # An KernelArguments object with both keyword arguments and execution_settings should return True
    assert KernelArguments(input=10, settings=PromptExecutionSettings(service_id="test"))
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
<<<<<<< HEAD
=======
=======
>>>>>>> f40c1f2075e2443c31c57c34f5f66c2711a8db75
>>>>>>> main
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
