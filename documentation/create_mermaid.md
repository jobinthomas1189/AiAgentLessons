# create_mermaid.py

**Location:** `utils/create_mermaid.py`

## Overview

Generates Mermaid diagram images for each LangGraph lesson file. Produces `.png` files in the `utils` directory for documentation and visualization.

## Purpose

- Extract Mermaid diagram strings from compiled LangGraphs
- Render graphs as PNG images via the Mermaid.INK API
- Support all lesson scripts: 01_quickstart through 07_handoffs

## Key Functions

### `get_mermaid_for_graph(graph) -> str`

Extracts the Mermaid flowchart string from a compiled LangGraph using `graph.get_graph().draw_mermaid()`.

### `save_mermaid_png(graph, output_path) -> bool`

Saves the graph as a PNG image. Uses Mermaid.INK API (requires network access). Returns `True` on success.

### `build_and_save_mermaid(name, graph, output_dir, print_mermaid, save_png) -> tuple[str, bool]`

Convenience function that generates Mermaid, optionally saves PNG, and optionally prints the Mermaid string.

## Graphs Generated

| Output File | Description |
|-------------|-------------|
| `01_quickstart.png` | Calculator agent (LLM + tool loop) |
| `02_persistence.png` | Simple node_a → node_b flow |
| `03_interrupts_approval.png` | Approval workflow with interrupt |
| `03_interrupts_review.png` | Review-and-edit flow |
| `03_interrupts_multi.png` | Parallel branches with interrupts |
| `04_durable_execution.png` | node_a → node_b with checkpointing |
| `05_multi_agent.png` | Router → coding/math/general agents |
| `06_subgraphs.png` | Parent graph with subgraph node |
| `07_handoffs.png` | Sales ↔ Support handoff flow |

## Usage

```bash
# From agentic_files directory
python utils/create_mermaid.py

# Or from utils directory
python create_mermaid.py
```

## Requirements

- **Network access** — PNG generation uses Mermaid.INK API
- LangGraph and related dependencies installed
- All lesson modules import successfully

## Output

- PNG files written to `utils/` directory
- Summary printed: `Saved X/Y graphs to <path>`
