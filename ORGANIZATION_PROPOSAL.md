# Repository Reorganization Proposal

This document proposes a cleaner, purpose‑driven directory structure for the repository while enabling a **phased, low‑risk migration**. No files are physically moved yet; this is a blueprint plus validation tooling.

## Goals

1. Reduce cognitive load at repo root (too many standalone scripts & Markdown files).
2. Make user journeys obvious (getting started, samples, automation, dev tools).
3. Separate operational automation from demos and from one‑off maintenance scripts.
4. Provide an auditable mapping + drift detection without breaking existing workflows immediately.
5. Keep backward compatibility via a deprecation window & shim launchers when moves occur.

## Current Pain Points (Summary)

- 70+ root‑level Python / shell scripts with mixed purposes.
- Mixed naming (demo*\*, test*\_, run\_\_, setup\__, _\_fix.py) blurs intent.
- Several parallel "README" style docs (README.md, README-ENHANCED.md, README*LOCAL_AI.md, AGI*\* docs) not grouped.
- Environment/setup scripts dispersed (quick_setup.py, setup-env.sh, setup_environment.py, workspace_quick_setup.py, etc.).
- Automation & maintenance scripts interleaved with experimental demos.

## Proposed Top-Level Layout (Target State)

```
01-core-implementations/           # (existing)
02-ai-workspace/                   # (existing)
... (keep numbered domain dirs)
docs/                              # High-level conceptual & guides (consolidated pointers)
docs/guides/                       # Thematic guides (AI, Local, Deployment)
docs/agi/                          # AGI-specific documents
samples/                           # End-user runnable examples (was scattered demos/*, demo_* scripts)
samples/agents/
samples/local_ai/
scripts/                           # Thin wrappers / launchers (CLI entry points)
tools/                             # Maintenance & reporting utilities (one-off / ops)
tools/automation/                  # Recurrent automation (workflows, attribution, copyright)
tools/environment/                 # Env + setup helpers
tools/quality/                     # Lint, audit, structure validators
internal/experimental/             # Incubating experiments (optional; gate by README)
tests/                             # (keep; move stray test_* root scripts inside if not already)
infrastructure/                    # Deployment / infra (could alias existing numbered dirs later)
```

## Classification Heuristics

| Category          | Criteria                          | Examples (current names)                                                                   |
| ----------------- | --------------------------------- | ------------------------------------------------------------------------------------------ |
| samples           | Teaches usage; safe to run; small | `demo_local_ai.py`, `demo_agi_agents.sh`, `ai_demo.md`, `demo_ai_types.md`                 |
| scripts           | User entry points / launchers     | `run.py`, `unified_launcher.py`, `master_launcher.py`                                      |
| tools/automation  | Batch / scheduled automation      | `automation_cli.py`, `automation_status_dashboard.py`, `final_workflow_fix.py`             |
| tools/quality     | Audits / validations              | `gitignore_audit.ipynb`, `organize_repo_comprehensive.py`, `repository_status_report.json` |
| tools/environment | Setup & env mgmt                  | `setup_environment.py`, `quick_setup.py`, `setup_local_ai.py`                              |
| tools/ops (alt)   | Maintenance fix scripts           | `fix_github_workflows.py`, `fix_workflows.sh`, `fix_symbolic_links.sh`                     |
| experimental      | Highly volatile prototypes        | `fake_local_llm.py`, ad‑hoc notebooks                                                      |

## Mapping & Migration Status (Updated)

Current tracked set (evolving). Status reflects validator output after Phase 2 partial migration.

| Legacy File                      | Target Location                                | Status / Action        | Notes / Rationale                               |
| -------------------------------- | ---------------------------------------------- | ---------------------- | ----------------------------------------------- |
| `demo_local_ai.py`               | `samples/local_ai/demo_local_ai.py`            | shim (migrated)        | Pure sample relocated with backward shim        |
| `demo_local_agents.py`           | `samples/agents/demo_local_agents.py`          | shim (migrated)        |                                                 |
| `demo_ai_types.md`               | `samples/ai_types/README.md`                   | duplicate (stub ptr)   | Root now stub pointer; will remove after window |
| `ai_demo.md`                     | `samples/README.md`                            | shim (stub)            | Root stub pointing to consolidated README       |
| `ai_markdown_demo.md`            | `samples/markdown/README.md`                   | shim (stub)            | Consolidated markdown demos                     |
| `run.py`                         | `scripts/run.py`                               | shim (migrated)        | Entry launcher                                  |
| `unified_launcher.py`            | `scripts/unified_launcher.py`                  | duplicate (needs shim) | Target placeholder exists; root to trim further |
| `master_launcher.py`             | `scripts/master_launcher.py`                   | duplicate (needs shim) | Consider future rename/deprecation              |
| `local_agent_launcher.py`        | `scripts/local_agent_launcher.py`              | shim (migrated)        | Newly added to mapping                          |
| `automation_cli.py`              | `tools/automation/automation_cli.py`           | pending                | Not migrated yet                                |
| `automation_status_dashboard.py` | `tools/automation/status_dashboard.py`         | pending                | Pending rename + move                           |
| `setup_environment.py`           | `tools/environment/setup_environment.py`       | pending (shim ready)   | Root shim present; target placeholder to add    |
| `quick_setup.py`                 | `tools/environment/quick_setup.py`             | shim (migrated)        |                                                 |
| `setup_local_ai.py`              | `tools/environment/setup_local_ai.py`          | duplicate              | Root shim + fuller target still in progress     |
| `workspace_quick_setup.py`       | `tools/environment/workspace_quick_setup.py`   | shim (migrated)        |                                                 |
| `organize_repo_comprehensive.py` | `tools/quality/organize_repo_comprehensive.py` | pending                | Quality tool not yet relocated                  |
| `fake_local_llm.py`              | `internal/experimental/fake_local_llm.py`      | pending                | Will mark experimental                          |

Legend: pending = only legacy present; shim = legacy retained only as thin wrapper/stub; duplicate = both legacy full content & target exist; migrated = target only (legacy removed).

Planned next batch: automation + quality + experimental consolidation; then remove remaining duplicates after stability window.

## Phased Migration Plan

1. (Current) Publish proposal + validator (non‑enforcing). Gather feedback.
2. Add empty target directories + README stubs (signals upcoming structure).
3. Move lowest‑risk pure samples (no imports depended upon elsewhere). Provide symlink or stub import wrappers ("shims") for 2 release cycles.
4. Migrate environment + automation tooling; update CI scripts referencing old paths.
5. Deprecate legacy root scripts (emit warning if executed) – remove after grace period.

## Backward Compatibility Shims (When Moving)

Pattern for Python script moved from root to `scripts/`:

```python
# Legacy shim – scheduled for removal after 2025-12-31
from scripts.run import main
if __name__ == "__main__":
    print("[DEPRECATION] Use 'python -m scripts.run' instead (will be removed after 2025-12-31).")
    main()
```

## Drift Validation Tool

`tools/quality/validate_structure.py` (added in this PR) will:

- Load the mapping table embedded in code.
- Warn (not fail) if a mapped file exists in old location and not in new.
- Provide `--json` output for CI informational job.

## Risks & Mitigations

| Risk                               | Mitigation                                                            |
| ---------------------------------- | --------------------------------------------------------------------- |
| Broken CI referencing moved paths  | Introduce moves only after search audit; update workflows in same PR. |
| Developer muscle memory friction   | Shims + deprecation messaging.                                        |
| Scope creep (moving everything)    | Phase gating; only batches with review.                               |
| Inconsistent partially-moved state | Validator highlights incomplete transitions.                          |

## Next Steps Checklist

- [ ] Collect maintainer feedback on categories.
- [ ] Add README stubs to new dirs.
- [ ] Implement first batch (samples) + shims.
- [ ] Update CI and docs referencing changed paths.
- [ ] Monitor validator output for 2 weeks.

### Suggested Command Snippets (Once Approved)

Create skeletal directories (idempotent):

```
mkdir -p samples/agents samples/local_ai samples/ai_types samples/markdown \
    scripts tools/automation tools/automation/markdown tools/environment \
    tools/quality/internal reports internal/experimental tools/ops
```

Run validator in JSON mode for CI artifact:

```
python tools/quality/validate_structure.py --json > structure_report.json
```

Example shim (commit alongside move):

```
echo "from scripts.run import main;\nif __name__ == '__main__':\n    print('[DEPRECATION] Use python -m scripts.run'); main()" > run.py
```

Automated batch move (dry run first):

```
python - <<'PY'
import shutil, json, os
mapping=json.loads('''{
    "demo_local_ai.py":"samples/local_ai/demo_local_ai.py"
}''')
for src,dst in mapping.items():
    if not os.path.exists(src):
        continue
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    print(f"MOVE {src} -> {dst}")
    # shutil.move(src,dst)  # uncomment when ready
PY
```

---

Generated proposal (date: 2025-08-09). Adjust timelines as needed.
