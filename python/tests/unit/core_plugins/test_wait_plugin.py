<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
# Copyright (c) Microsoft. All rights reserved.

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
<<<<<<< HEAD
# Copyright (c) Microsoft. All rights reserved.

=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
# Copyright (c) Microsoft. All rights reserved.

=======
>>>>>>> Stashed changes
=======
# Copyright (c) Microsoft. All rights reserved.

=======
>>>>>>> Stashed changes
>>>>>>> head
<<<<<<< main
# Copyright (c) Microsoft. All rights reserved.

=======
>>>>>>> ms/small_fixes
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< HEAD
>>>>>>> main
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
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> head
from unittest.mock import patch

import pytest

from semantic_kernel.core_plugins.wait_plugin import WaitPlugin
from semantic_kernel.exceptions import FunctionExecutionException

test_data_good = [
    0,
    1.0,
    -2,
    "0",
    "1",
    "2.1",
    "0.1",
    "0.01",
    "0.001",
    "0.0001",
    "-0.0001",
]

test_data_bad = [
    "$0",
    "one hundred",
    "20..,,2,1",
    ".2,2.1",
    "0.1.0",
    "00-099",
    "¹²¹",
    "2²",
    "zero",
    "-100 seconds",
    "1 second",
]


def test_can_be_instantiated():
    plugin = WaitPlugin()
    assert plugin is not None


@pytest.mark.parametrize("wait_time", test_data_good)
async def test_wait_valid_params(wait_time):
    plugin = WaitPlugin()
    with patch("asyncio.sleep") as patched_sleep:
        await plugin.wait(wait_time)

<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        patched_sleep.assert_called_once_with(abs(float(wait_time)))
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
<<<<<<< HEAD
        patched_sleep.assert_called_once_with(abs(float(wait_time)))
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
        patched_sleep.assert_called_once_with(abs(float(wait_time)))
=======
>>>>>>> Stashed changes
=======
        patched_sleep.assert_called_once_with(abs(float(wait_time)))
=======
>>>>>>> Stashed changes
>>>>>>> head
<<<<<<< main
        patched_sleep.assert_called_once_with(abs(float(wait_time)))
=======
        assert patched_sleep.called_once_with(abs(float(wait_time)))
>>>>>>> ms/small_fixes
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< HEAD
>>>>>>> main
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
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> head


@pytest.mark.parametrize("wait_time", test_data_bad)
async def test_wait_invalid_params(wait_time):
    plugin = WaitPlugin()

    with pytest.raises(FunctionExecutionException) as exc_info:
        await plugin.wait("wait_time")

    assert exc_info.value.args[0] == "seconds text must be a number"
