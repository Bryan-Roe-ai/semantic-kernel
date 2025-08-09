"""Repository structure validator (non-enforcing).

Usage:
  python tools/quality/validate_structure.py [--json]

Outputs warnings if files identified for relocation (per proposal) still
exist only in legacy locations or if duplicates appear in both old & new.

Exit codes:
  0 = Completed (informational only)
"""
from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass, asdict
from typing import Dict, List


# Minimal mapping snapshot (expand over time)
MAPPING: Dict[str, str] = {
    "demo_local_ai.py": "samples/local_ai/demo_local_ai.py",
    "demo_local_agents.py": "samples/agents/demo_local_agents.py",
    "demo_ai_types.md": "samples/ai_types/README.md",
    "ai_demo.md": "samples/README.md",
    "ai_markdown_demo.md": "samples/markdown/README.md",
    "run.py": "scripts/run.py",
    "unified_launcher.py": "scripts/unified_launcher.py",
    "master_launcher.py": "scripts/master_launcher.py",
    "local_agent_launcher.py": "scripts/local_agent_launcher.py",
    "automation_cli.py": "tools/automation/automation_cli.py",
    "automation_status_dashboard.py": "tools/automation/status_dashboard.py",
    "setup_environment.py": "tools/environment/setup_environment.py",
    "quick_setup.py": "tools/environment/quick_setup.py",
    "setup_local_ai.py": "tools/environment/setup_local_ai.py",
    "workspace_quick_setup.py": "tools/environment/workspace_quick_setup.py",
    "organize_repo_comprehensive.py": "tools/quality/organize_repo_comprehensive.py",
    "fake_local_llm.py": "internal/experimental/fake_local_llm.py",
}


@dataclass
class FileStatus:
    legacy: str
    target: str
    legacy_exists: bool
    target_exists: bool
    status: str  # "pending", "migrated", "duplicate", "missing", "shim"
    shim: bool


def is_shim(path: str) -> bool:
    """Heuristic to detect deprecation shim wrappers.

    Criteria:
      - File size < 2.5 KB
      - Contains 'Deprecation shim' or '[DEPRECATION]' and 'moved to'
    """
    try:
        if not os.path.isfile(path):
            return False
        if os.path.getsize(path) > 2500:
            return False
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read(2048)
        markers = ["moved to", "DEPRECATION", "shim"]
        return sum(m in text for m in markers) >= 2
    except OSError:
        return False


def evaluate(repo_root: str) -> List[FileStatus]:
    results: List[FileStatus] = []
    for legacy, target in MAPPING.items():
        legacy_path = os.path.join(repo_root, legacy)
        target_path = os.path.join(repo_root, target)
        legacy_exists = os.path.exists(legacy_path)
        target_exists = os.path.exists(target_path)
        shim_flag = legacy_exists and is_shim(legacy_path)
        if legacy_exists and not target_exists:
            state = "pending"
        elif not legacy_exists and target_exists:
            state = "migrated"
        elif shim_flag and target_exists:
            state = "shim"
        elif legacy_exists and target_exists:
            state = "duplicate"
        else:
            state = "missing"
        results.append(FileStatus(legacy, target, legacy_exists, target_exists, state, shim_flag))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate repository structure against proposal.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON report")
    args = parser.parse_args()
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    statuses = evaluate(repo_root)

    pending = [s for s in statuses if s.status == "pending"]
    duplicate = [s for s in statuses if s.status == "duplicate"]
    shims = [s for s in statuses if s.status == "shim"]

    if args.json:
        print(json.dumps([asdict(s) for s in statuses], indent=2))
    else:
        print("Repository Structure Validation (informational)\n")
        for s in statuses:
            print(f"- {s.legacy} -> {s.target} : {s.status}")
        print("\nSummary:")
        print(f"  Pending moves : {len(pending)}")
        print(f"  Shims         : {len(shims)}")
        print(f"  Duplicates    : {len(duplicate)}")
        print(f"  Total tracked : {len(statuses)}")
        if duplicate:
            print("\n[Warning] Some files exist in both legacy and target paths – remove legacy copies after verification.")
    return 0


if __name__ == "__main__":  # pragma: no cover - simple CLI wrapper
    raise SystemExit(main())
