#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LANGGRAPH_CONFIG="${SCRIPT_DIR}/langgraph.json"

# Number (0-7) maps to matching index in this list.
GRAPH_TARGETS=(
  "./agentic_files/server_graph_registry.py:graph_00_server_graph"
  "./agentic_files/server_graph_registry.py:graph_01_quickstart"
  "./agentic_files/server_graph_registry.py:graph_02_persistence"
  "./agentic_files/server_graph_registry.py:graph_03_interrupts"
  "./agentic_files/server_graph_registry.py:graph_04_durable_execution"
  "./agentic_files/server_graph_registry.py:graph_05_multi_agent"
  "./agentic_files/server_graph_registry.py:graph_06_subgraphs"
  "./agentic_files/server_graph_registry.py:graph_07_handoffs"
)

print_usage() {
  echo "Usage: ./run_langgraph_server.sh <0-7> [--set-only|--run]"
  echo
  for i in "${!GRAPH_TARGETS[@]}"; do
    printf "  %s -> %s\n" "$i" "${GRAPH_TARGETS[$i]}"
  done
}

if [[ $# -lt 1 || $# -gt 2 ]]; then
  print_usage
  exit 1
fi

GRAPH_INDEX="$1"
if ! [[ "${GRAPH_INDEX}" =~ ^[0-9]+$ ]] || (( GRAPH_INDEX < 0 || GRAPH_INDEX >= ${#GRAPH_TARGETS[@]} )); then
  echo "Error: graph index must be a number from 0 to 7."
  print_usage
  exit 1
fi

MODE="${2:---run}"
if [[ "${MODE}" != "--set-only" && "${MODE}" != "--run" ]]; then
  echo "Error: second argument must be --set-only or --run."
  print_usage
  exit 1
fi

GRAPH_TARGET="${GRAPH_TARGETS[$GRAPH_INDEX]}"

python3 - "${LANGGRAPH_CONFIG}" "${GRAPH_TARGET}" <<'PY'
import json
import sys
from pathlib import Path

config_path = Path(sys.argv[1])
graph_target = sys.argv[2]

config = json.loads(config_path.read_text(encoding="utf-8"))
config.setdefault("graphs", {})
config["graphs"]["calculator"] = graph_target
config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
PY

echo "Updated langgraph.json -> graphs.calculator = ${GRAPH_TARGET}"

if [[ "${MODE}" == "--set-only" ]]; then
  echo "Set-only mode complete."
  exit 0
fi

echo "Starting LangGraph dev server..."
exec langgraph dev
