"""Prompt registry placeholder."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict

@dataclass
class PromptTemplate:
    name: str
    version: str
    text: str

class PromptRegistry:
    def __init__(self):
        self._prompts: Dict[str, PromptTemplate] = {}

    def register(self, prompt: PromptTemplate) -> None:
        key = f"{prompt.name}:{prompt.version}"
        self._prompts[key] = prompt

    def get(self, name: str, version: str) -> PromptTemplate | None:
        return self._prompts.get(f"{name}:{version}")

    def list(self):
        return list(self._prompts.values())
