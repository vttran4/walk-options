#!/usr/bin/env bash
set -euo pipefail

# Start API
uvicorn api:app --reload &
API_PID=$!

# Start Streamlit UI
streamlit run app.py &
UI_PID=$!

cleanup() {
  kill "$API_PID" "$UI_PID" 2>/dev/null || true
}

trap cleanup EXIT

wait "$API_PID" "$UI_PID"
