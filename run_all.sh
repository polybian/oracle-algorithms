#!/usr/bin/env bash
# Runs every implementation in order.
set -euo pipefail
cd "$(dirname "$0")"

# Prefer the project's venv (where qiskit lives); fall back to python3.
if [ -x ".venv/bin/python" ]; then
  PY=".venv/bin/python"
else
  PY="python3"
fi

echo "=== 01 — Bernstein-Vazirani (hidden string in 1 query) ==="
$PY scripts/01_bernstein_vazirani.py
echo
echo "=== 02 — Simon (hidden period via linear equations) ==="
$PY scripts/02_simon.py
echo
echo "=== 03 — Query advantage table ==="
$PY scripts/03_query_advantage.py
echo
echo "All three implementations completed successfully."
