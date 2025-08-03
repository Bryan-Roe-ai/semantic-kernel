#!/usr/bin/env python3
"""Utility helpers to create mock environments for agent tests."""

from contextlib import contextmanager
import os
from typing import Dict, Iterator


@contextmanager
def apply_env(env: Dict[str, str]) -> Iterator[None]:
    """Temporarily apply environment variables."""
    original = {key: os.environ.get(key) for key in env}
    try:
        os.environ |= env
        yield
    finally:
        for key, value in original.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def openai_env(**overrides: str) -> Dict[str, str]:
    """Return a dictionary of mock OpenAI environment variables."""
    env = {
        "OPENAI_API_KEY": "sk-test",
        "OPENAI_CHAT_MODEL_ID": "gpt-mock",
        "OPENAI_ORG_ID": "org-mock",
    } | overrides
    return env


def azure_openai_env(**overrides: str) -> Dict[str, str]:
    """Return a dictionary of mock Azure OpenAI environment variables."""
    env = {
        "AZURE_OPENAI_API_KEY": "test-key",
        "AZURE_OPENAI_ENDPOINT": "https://example.azure.com",
        "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME": "gpt-mock",
        "AZURE_OPENAI_API_VERSION": "2024-02-01",
    }
    env.update(overrides)
    return env


@contextmanager
def mock_openai_environment(**overrides: str) -> Iterator[None]:
    """Context manager applying mock OpenAI settings."""
    with apply_env(openai_env(**overrides)):
        yield


@contextmanager
def mock_azure_openai_environment(**overrides: str) -> Iterator[None]:
    """Context manager applying mock Azure OpenAI settings."""
    with apply_env(azure_openai_env(**overrides)):
        yield
