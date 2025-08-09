"""Heuristic diff risk scorer (placeholder)."""
from __future__ import annotations
from typing import Sequence

PROTECTED_PATHS = ["agi/", "semantic_kernel/"]


def score_diff(changed_files: Sequence[str], lines_added: int, lines_deleted: int) -> tuple[float, str]:
    risk = 0.0
    rationale_parts = []
    footprint = lines_added + lines_deleted
    if footprint > 500:
        risk += 0.3
        rationale_parts.append("Large footprint")
    if any(f.startswith(tuple(PROTECTED_PATHS)) for f in changed_files):
        risk += 0.4
        rationale_parts.append("Touches protected path")
    if any(f.endswith(('.py', '.cs')) for f in changed_files):
        risk += 0.1
        rationale_parts.append("Code files modified")
    if len(changed_files) > 10:
        risk += 0.2
        rationale_parts.append("Many files changed")
    return min(risk, 1.0), "; ".join(rationale_parts) or "Low risk"
