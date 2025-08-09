"""Evaluation runner stub.
Loads benchmark YAML task specs and executes dummy success criteria for now.
"""
from __future__ import annotations
try:  # Optional dependency
    import yaml  # type: ignore
except Exception:  # pragma: no cover - fallback mode
    yaml = None  # type: ignore
from pathlib import Path
from typing import List, Dict, Any
import time, json
from agi.telemetry import telemetry
from agi.planner.static_planner import StaticPlanner

class EvaluationResult(Dict[str, Any]):
    pass

def _fallback_parse(text: str) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    current_list_key: str | None = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line or line.strip().startswith("#"):
            continue
        if line.startswith("  - ") and current_list_key:
            data.setdefault(current_list_key, []).append(line[4:].strip())
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"')
            if value == "":
                # assume list starts next lines
                current_list_key = key
                data[key] = []
            else:
                current_list_key = None
                data[key] = value
    return data

def load_benchmarks(path: str | Path) -> List[Dict[str, Any]]:
    tasks: List[Dict[str, Any]] = []
    for p in Path(path).glob("*.yml"):
        with open(p, "r", encoding="utf-8") as f:
            text = f.read()
        if yaml:
            try:
                tasks.append(yaml.safe_load(text))  # type: ignore
                continue
            except Exception:
                pass
        tasks.append(_fallback_parse(text))
    return tasks

@telemetry("run_benchmarks")
def run_benchmarks(path: str | Path, output_metrics: str | None = None) -> List[EvaluationResult]:
    results: List[EvaluationResult] = []
    tasks = load_benchmarks(path)
    planner = StaticPlanner()
    for t in tasks:
        start = time.time()
        goal = t.get("goal", "")
        plan_steps = planner.propose(goal, {})
        iterations = len(plan_steps)
        expect = t.get("expect_contains", "")
        # Placeholder execution: success if expect substring in goal
        success = expect.lower() in goal.lower() if expect else True
        latency = time.time() - start
        result: EvaluationResult = EvaluationResult(
            task_id=t.get("id"),
            success=success,
            latency_ms=int(latency * 1000),
            planner_strategy="static",
            steps=iterations,
        )
        results.append(result)
    if output_metrics:
        with open(output_metrics, "a", encoding="utf-8") as f:
            for r in results:
                f.write(json.dumps(r) + "\n")
    return results
