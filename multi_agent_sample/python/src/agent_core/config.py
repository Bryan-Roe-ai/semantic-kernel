from __future__ import annotations

from pydantic import BaseModel


class AgentSettings(BaseModel):
    """Basic configuration for an Agent.

    Extend with model provider, temperature, memory store references, etc.
    """

    default_prefix: str = "Agent"
    echo_format: str = "{name}: {message}"  # template for echo mode
