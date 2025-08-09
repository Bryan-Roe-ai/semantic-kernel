"""Planner interfaces and data structures."""
from __future__ import annotations
from typing import Protocol, TypedDict, List, Dict, Any

class PlanStep(TypedDict):
    id: str
    action: str  # tool or sub-agent name
    input: str
    rationale: str
    cost_estimate: float

class Planner(Protocol):
    def propose(self, goal: str, context: Dict[str, Any]) -> List[PlanStep]:
        """Return an initial list of plan steps to attempt for a goal."""
        ...

    def refine(self, feedback: Dict[str, Any]) -> List[PlanStep]:
        """Incorporate feedback (success/failure metrics) and adjust plan."""
        ...
