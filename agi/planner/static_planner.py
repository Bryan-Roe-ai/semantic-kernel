"""Static baseline planner implementation.
Produces a deterministic 1-3 step plan based on simple heuristics.
"""
from __future__ import annotations
from typing import Dict, Any, List
from .interface import Planner, PlanStep
from agi.telemetry import telemetry, approximate_tokens

class StaticPlanner:
    def __init__(self, max_steps: int = 3):
        self.max_steps = max_steps

    @telemetry("planner_propose", context_fn=lambda self, goal, context: {"strategy": "static", "goal_tokens": approximate_tokens(goal)})
    def propose(self, goal: str, context: Dict[str, Any]) -> List[PlanStep]:  # type: ignore[override]
        steps: List[PlanStep] = []
        normalized = goal.lower()
        if "report" in normalized:
            steps.append(self._make_step("analyze_goal", goal, "Understand report scope"))
            steps.append(self._make_step("collect_data", goal, "Gather required inputs"))
            steps.append(self._make_step("generate_report", goal, "Synthesize and format output"))
        else:
            steps.append(self._make_step("analyze_goal", goal, "Clarify intent"))
            if "optimize" in normalized:
                steps.append(self._make_step("collect_metrics", goal, "Gather performance metrics"))
                steps.append(self._make_step("apply_optimization", goal, "Apply changes"))
            else:
                steps.append(self._make_step("execute_action", goal, "Single action execution"))
        return steps[: self.max_steps]

    @telemetry("planner_refine", context_fn=lambda self, feedback: {"strategy": "static"})
    def refine(self, feedback: Dict[str, Any]) -> List[PlanStep]:  # type: ignore[override]
        # Static planner does not adapt; returns empty indicating no refinement.
        return []

    def _make_step(self, action: str, input_text: str, rationale: str) -> PlanStep:
        idx = action + "_1"
        return {
            "id": idx,
            "action": action,
            "input": input_text,
            "rationale": rationale,
            "cost_estimate": 1.0,
        }
