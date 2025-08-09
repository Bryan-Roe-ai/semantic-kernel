"""Lightweight unit tests for AGI modules (no external deps).
Run: python test_agi_unit.py
"""
from agi.planner.static_planner import StaticPlanner
from agi.memory.store import MemoryStore, MemoryItem
from agi.safety.diff_risk import score_diff
from agi.evaluation.runner import run_benchmarks
from pathlib import Path
import os, json, tempfile, shutil
from scripts.run_evaluation_gate import main as eval_main, BASELINE_FILE


def test_planner():
    p = StaticPlanner()
    steps = p.propose("Generate a summary report", {})
    assert steps, "Planner should return steps"
    assert steps[0]["action"] == "analyze_goal"

def test_memory_similarity():
    store = MemoryStore()
    store.upsert(MemoryItem(id="1", text="System architecture overview", metadata={}))
    store.upsert(MemoryItem(id="2", text="Unrelated note", metadata={}))
    res = store.similar("architecture", k=2)
    assert res and res[0][0].id == "1"

def test_diff_risk():
    score, rationale = score_diff(["agi/planner/static_planner.py"], 10, 2)
    assert 0 <= score <= 1 and rationale


def test_evaluation_runner():
    results = run_benchmarks(Path("benchmarks"))
    assert results, "Should load benchmark tasks"

def test_force_baseline_logic():
    # Use temp dir to avoid polluting repo baseline
    cwd = os.getcwd()
    tmp = tempfile.mkdtemp()
    try:
        os.chdir(tmp)
        # Copy benchmarks dir reference (symlink or minimal stub)
        # For simplicity, just create empty baseline absence scenario
        os.environ["GITHUB_REF"] = "refs/heads/main"
        if "AGI_FORCE_BASELINE" in os.environ:
            del os.environ["AGI_FORCE_BASELINE"]
        # Run evaluation once to create baseline
        code1 = eval_main()
        assert BASELINE_FILE.exists(), "Baseline should be created on main when absent"
        baseline_content = json.loads(BASELINE_FILE.read_text())
        # Force overwrite
        os.environ["AGI_FORCE_BASELINE"] = "1"
        code2 = eval_main()
        assert BASELINE_FILE.exists(), "Baseline should exist after force"
        new_content = json.loads(BASELINE_FILE.read_text())
        assert baseline_content == new_content, "Forced run should still produce valid baseline JSON"
        assert code1 in (0,1) and code2 in (0,1)
    finally:
        os.chdir(cwd)
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    failed = []
    for fn in [test_planner, test_memory_similarity, test_diff_risk, test_evaluation_runner, test_force_baseline_logic]:
        try:
            fn()
            print(f"PASS {fn.__name__}")
        except Exception as e:  # pragma: no cover
            failed.append((fn.__name__, e))
            print(f"FAIL {fn.__name__}: {e}")
    if failed:
        raise SystemExit(1)
