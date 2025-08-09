# Semantic Kernel Fork – AI Agent Instructions

> Pruned quick-start guidance for AI automation. Focus on what’s unique here; generic advice intentionally omitted.

## Quick Essentials
* Multi-language: core implementations in `01-core-implementations/` (python, dotnet, java placeholder).
* Python core: `semantic_kernel/` with `connectors/ai/*` and `connectors/memory_stores/*`.
* .NET solution: `dotnet/SK-dotnet.sln` (Core, Connectors.*, Plugins.*, Experimental.*, Planners, Extensions).
* Experimental flags via `SEMANTIC_KERNEL_EXPERIMENTAL_FEATURES` (SKEXP####) – never silently enable new behavior.
* Build tasks (VS Code): Python build/test, .NET build/test, MCP integration tests, environment setup script.
* Env setup: run `setup_environment.py` to create `.env.template` & config; never hardcode secrets.
* Agents lifecycle: Created → Active → Suspended → Resumed → Deleted (see AGENT_LIFECYCLE doc).
* Memory stores follow consistent CRUD + similarity interface; mirror an existing store when adding new.
* Prefer async patterns & reuse InternalUtilities (C#) for HTTP/diagnostics; avoid reinventing.
* Cross-language parity: changes to public abstractions require Python + .NET updates (and later Java).

## Structure & Conventions
* Python: Ruff + MyPy (types, 120 cols). Keep unit tests focused & fast.
* C#: Nullable enabled; XML docs for new public APIs; use `[Experimental]` for SKEXP surfaces.
* Feature addition: add tests + docs snippet + optional sample; guard with flag if unstable.
* Memory store naming: Python `connectors/memory_stores/<store>`; C# `Connectors.Memory.<Store>` project.
* Prompt/template engines go under existing extensions; avoid duplicating templating logic.
* Logging: reuse existing logging patterns; avoid verbose default INFO logs in tight loops.

## Build & Test
* Python: task “Build Semantic Kernel (Python)” (poetry install) then “Test Semantic Kernel (Python)” (pytest).
* .NET: tasks build/test `SK-dotnet.sln`.
* All + MCP: “Test All” orchestrates builds + unit + MCP integration.
* Before tests needing external AI: run `setup_environment.py` & set env vars.
* Keep new tests deterministic; skip network-dependent tests unless explicitly tagged.

## Agents & Memory Patterns
* Lifecycle hook usage: persist state on Suspend, restore on Resume; no new states.
* Adding memory store: replicate interface from an existing store (e.g. Redis) + CRUD + similarity; include minimal tests.
* Use existing retry/backoff config instead of custom loops.

## Performance & Observability
* Stream when possible; avoid buffering large responses.
* Leverage shared diagnostics utilities (C#) and consistent logging levels.
* Cache feature flag evaluation.

## Appendix A: Web Utilities
Open: `"$BROWSER" <url>` | Download: `curl -L -o file.html <url>` | Mirror: `wget --recursive --no-clobber --page-requisites --html-extension --convert-links <url>` | Extract: `curl -s <url> | grep -oP 'pattern'` | POST: `curl -X POST -H "Content-Type: application/json" -d '{"k":"v"}' <url>` | Headers: `curl -I <url>` | Status: `curl -w "%{http_code}" <url>` | Probe: `wget --spider <url>`

To open a webpage in the host's default browser, use:

`"$BROWSER" <url>`

For advanced web operations:

* Mirror site (respect robots): `wget --recursive --no-clobber --page-requisites --convert-links --adjust-extension <url>`
* Save HTML: `curl -s <url> -o page.html`
* Extract links: `curl -s <url> | grep -oP 'href="\K[^"]+' | sort -u`
* POST JSON: `curl -X POST -H "Content-Type: application/json" -d '{"ping":true}' <url>`
* Timing metrics: `curl -w 'DNS:%{time_namelookup} TCP:%{time_connect} TLS:%{time_appconnect} TTFB:%{time_starttransfer} Total:%{time_total} Code:%{http_code}\n' -o /dev/null -s <url>`
* Check size only: `curl -sI <url> | grep -i 'content-length'`
* Probe (no download): `wget --spider <url>`

Keep these out of fast unit tests; mock network I/O unless an integration tag is used.

## 11. Experimental Flags (Reference)
Pattern: `SKEXP####` (4 digits). Categories:
* 0000–0019: Core content evolution (chat/message structure).
* 0040–0059: API manifest & schema ingestion.
* 0060–0069: Planning / planners.
* 0070–0099: Connector families (Google, AzureAIInference, MistralAI, AssemblyAI, etc.).
* 0100–0119: Advanced/streaming content types.
Lifecycle:
1. Introduce: Add attribute/tag + doc line + gated usage.
2. Evaluate: Samples/tests may suppress warnings with `#pragma warning disable SKEXP####`.
3. Graduate: Remove flag gating & warning; update docs marking flag as stable.
4. Deprecate: Keep entry, mark as superseded; do not reassign numbers.
Examples in repo: `SKEXP0001`, `SKEXP0010`, `SKEXP0040`, `SKEXP0043`, `SKEXP0050`, `SKEXP0060`, `SKEXP0070`, `SKEXP0101`, `SKEXP0110`.
Addition process: choose next unused sequential number in category range, update mapping table, add minimal test proving guarded behavior, ensure environment flag `SEMANTIC_KERNEL_EXPERIMENTAL_FEATURES` enables it (comma-separated).

## 17. Java Contribution Kickoff
Goal: Incremental parity baseline.
Milestones:
1. Core kernel primitives (context, function registry, invocation pipeline).
2. Chat completion connector (OpenAI/Azure) + streaming stub.
3. Embeddings + simple in-memory memory store.
4. Prompt template loading + minimal planner (if SKEXP0060 active).
5. Additional high-demand connectors + persistence abstractions.
Contributing:
* Layout: `01-core-implementations/java/` with Gradle Kotlin DSL, `examples/`.
* Package: `com.microsoft.semantickernel` (fork may prefix). Mirror naming from other languages.
* Each public API: verify parity; open tracking issue if temporary gap.
* Tests: JUnit5, deterministic; avoid real network unless tagged.
* Experimental: implement only if stable elsewhere or explicitly exploring; reuse same SKEXP id.
* Docs: README with parity matrix + feature status.
Definition of done: code + unit test + (if user-facing) example + doc snippet + (if experimental) flag doc entry.
Initial exclusions: advanced external memory stores, complex multi-step planning heuristics, schema ingestion APIs (SKEXP0040+).
If divergence required: add `// PARITY_NOTE:` with rationale + issue link.
Quality gate: `./gradlew build` passes, no new warnings on public APIs.
