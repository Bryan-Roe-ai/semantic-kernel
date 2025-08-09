#!/usr/bin/env bash
set -euo pipefail

echo "[test_all] Building Python project"
if [ -d python ]; then
  (cd python && if command -v poetry >/dev/null 2>&1; then poetry install; else pip install -r requirements.txt || true; fi)
fi

echo "[test_all] Building .NET solution"
if [ -d dotnet ]; then
  dotnet build dotnet/SK-dotnet.sln /property:GenerateFullPaths=true /consoleloggerparameters:NoSummary
fi

echo "[test_all] Running Python unit tests with coverage"
if [ -d python ]; then
  (
    cd python
    if command -v poetry >/dev/null 2>&1; then
      poetry run pytest tests/unit -v \
        --cov=semantic_kernel \
        --cov-report=xml:coverage.xml \
        --junit-xml=pytest.xml || PY_TEST_STATUS=$?
    else
      python -m pytest tests/unit -v \
        --cov=semantic_kernel \
        --cov-report=xml:coverage.xml \
        --junit-xml=pytest.xml || PY_TEST_STATUS=$?
    fi
  )
fi

echo "[test_all] Running .NET tests with coverage"
if [ -d dotnet ]; then
  dotnet test dotnet/SK-dotnet.sln \
    /property:GenerateFullPaths=true \
    /consoleloggerparameters:NoSummary \
    --logger "trx;LogFileName=dotnet-test-results.trx" \
    --collect:"XPlat Code Coverage" \
    --results-directory dotnet/TestResults || DOTNET_TEST_STATUS=$?
fi

# MCP integration test (starts server in background if needed)
if [ -f mcp_server.py ] && [ -f test_mcp_integration.py ]; then
  echo "[test_all] Starting MCP server (background)"
  python3 mcp_server.py &
  MCP_PID=$!
  sleep 2
  echo "[test_all] Running MCP integration test"
  python3 test_mcp_integration.py || { echo "MCP integration test failed"; kill $MCP_PID || true; exit 1; }
  kill $MCP_PID || true
fi

if [ "${PY_TEST_STATUS:-0}" != "0" ] || [ "${DOTNET_TEST_STATUS:-0}" != "0" ]; then
  echo "[test_all] One or more test suites failed (Python=${PY_TEST_STATUS:-0} .NET=${DOTNET_TEST_STATUS:-0})."
  exit 1
fi

echo "[test_all] All tests completed successfully"

echo "[test_all] Extracting coverage reports"
if [ -d python ]; then
  (
    cd python
    if command -v poetry >/dev/null 2>&1; then
      poetry run coverage xml -o coverage.xml
    else
      coverage xml -o coverage.xml
    fi
  )
fi

echo "[test_all] Summary of test results"
if [ -d dotnet ]; then
  dotnet test dotnet/SK-dotnet.sln --logger "console;verbosity=detailed"
fi

if [ -f python/pytest.xml ]; then
  echo "Python unit tests:"
  cat python/pytest.xml
fi

if [ -f dotnet/TestResults/dotnet-test-results.trx ]; then
  echo ".NET tests:"
  cat dotnet/TestResults/dotnet-test-results.trx
fi

      - name: Extract Coverage Metrics
        run: |
          python scripts/compute_coverage.py > cov_env.txt || true
          echo "Computed raw coverage environment lines:"
          cat cov_env.txt || true

          # Export (fall back to 0.00 if missing)
          grep '^PY_COV=' cov_env.txt >> "$GITHUB_ENV" || echo 'PY_COV=0.00' >> "$GITHUB_ENV"
          grep '^DN_COV=' cov_env.txt >> "$GITHUB_ENV" || echo 'DN_COV=0.00' >> "$GITHUB_ENV"
          grep '^COMBINED_COV=' cov_env.txt >> "$GITHUB_ENV" || echo 'COMBINED_COV=0.00' >> "$GITHUB_ENV"

          echo "Final exported values:"
          echo "PY_COV=${PY_COV:-}"
          echo "DN_COV=${DN_COV:-}"
          echo "COMBINED_COV=${COMBINED_COV:-}"

      - name: Summary
        run: |
          echo "## Coverage Summary" >> "$GITHUB_STEP_SUMMARY"
          echo "" >> "$GITHUB_STEP_SUMMARY"
          echo "| Target   | Coverage |" >> "$GITHUB_STEP_SUMMARY"
          echo "|----------|----------|" >> "$GITHUB_STEP_SUMMARY"
          [ -n "${PY_COV:-}" ] && echo "| Python   | ${PY_COV}% |" >> "$GITHUB_STEP_SUMMARY"
          [ -n "${DN_COV:-}" ] && echo "| .NET     | ${DN_COV}% |" >> "$GITHUB_STEP_SUMMARY"
          [ -n "${COMBINED_COV:-}" ] && echo "| Combined | ${COMBINED_COV}% |" >> "$GITHUB_STEP_SUMMARY"
