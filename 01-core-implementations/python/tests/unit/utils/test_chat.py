#!/usr/bin/env python3
"""
Test module for chat

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from unittest.mock import Mock

from semantic_kernel.utils.chat import store_results


def test_store_results():
    chat_history_mock = Mock()
    chat_history_mock.add_message = Mock()

    chat_message_content_mock = Mock()
    results = [chat_message_content_mock, chat_message_content_mock]

    updated_chat_history = store_results(chat_history_mock, results)

    assert chat_history_mock.add_message.call_count == len(results)
    for message in results:
        chat_history_mock.add_message.assert_any_call(message=message)

    assert updated_chat_history == chat_history_mock
