#!/usr/bin/env python3
"""Run benchmark suite and print KPI summary JSON.
Exit code 1 if thresholds not met (placeholder thresholds for now).
"""
from __future__ import annotations
import json, sys, statistics
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agi.evaluation.runner import run_benchmarks  # type: ignore  # noqa:E402

BENCH_DIR = Path(__file__).resolve().parents[1] / "benchmarks"
BASELINE_FILE = Path("baseline_kpis.json")
THRESHOLDS = {
    "task_success_rate": 0.5,  # placeholder
    "median_planning_iterations": 1,  # ensure at least single-step planning median
    "median_latency_ms": 0,  # allow raising later; 0 means no latency floor yet
    "p95_latency_ms": 0,  # placeholder; tighten later
}

def main() -> int:
    results = run_benchmarks(BENCH_DIR)
    if not results:
        print(json.dumps({"error": "no benchmarks found"}))
        return 1
    successes = sum(1 for r in results if r["success"]) / len(results)
    latencies = [r["latency_ms"] for r in results]
    planning_iters = [r.get("steps", 0) for r in results]
    # Simple p95 computation
    sorted_lat = sorted(latencies)
    p95_index = int(0.95 * (len(sorted_lat) - 1)) if sorted_lat else 0
    p95_latency = sorted_lat[p95_index] if sorted_lat else 0
    kpis = {
        "task_success_rate": successes,
        "median_latency_ms": int(statistics.median(latencies)),
        "p95_latency_ms": int(p95_latency),
        "median_planning_iterations": int(statistics.median(planning_iters)) if planning_iters else 0,
        "count": len(results),
    }
    regression = False
    baseline_data = None
    import os
    force_baseline = os.environ.get("AGI_FORCE_BASELINE") == "1"
    if BASELINE_FILE.exists() and not force_baseline:
        try:
            baseline_data = json.loads(BASELINE_FILE.read_text())
            base_rate = baseline_data.get("task_success_rate")
            if base_rate is not None and kpis["task_success_rate"] < base_rate:
                regression = True
        except Exception:
            pass
    else:
        # Auto-capture baseline only on main branch (heuristic: env var GITHUB_REF == 'refs/heads/main')
        ref = os.environ.get("GITHUB_REF")
        if ref == "refs/heads/main":
            try:
                BASELINE_FILE.write_text(json.dumps({k: v for k, v in kpis.items() if k != "count"}, indent=2))
                baseline_data = json.loads(BASELINE_FILE.read_text())
            except Exception:
                pass
    output = {"kpis": kpis, "thresholds": THRESHOLDS, "regression": regression, "baseline": baseline_data}
    print(json.dumps(output, indent=2))
    # Threshold enforcement
    if (
        successes < THRESHOLDS["task_success_rate"]
        or kpis["median_planning_iterations"] < THRESHOLDS["median_planning_iterations"]
    or kpis["median_latency_ms"] < THRESHOLDS["median_latency_ms"]
    or kpis["p95_latency_ms"] < THRESHOLDS["p95_latency_ms"]
        or regression
    ):
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
