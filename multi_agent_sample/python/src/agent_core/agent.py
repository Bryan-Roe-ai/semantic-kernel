from __future__ import annotations

from dataclasses import dataclass, field

from .config import AgentSettings


@dataclass
class Agent:
    """A minimal Agent abstraction.

    For now it only echoes back messages; replace implementation with actual LLM or planner calls.
    """

    name: str
    settings: AgentSettings = field(default_factory=AgentSettings)

    def send_message(self, message: str) -> str:  # noqa: D401 - simple echo
        if not message:
            raise ValueError("message cannot be empty")
        return self.settings.echo_format.format(name=self.name, message=message)
