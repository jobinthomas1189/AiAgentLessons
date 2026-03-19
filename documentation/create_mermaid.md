# create_mermaid.py

**Location:** `agentic_files/utils/create_mermaid.py`

## Overview

Utility helpers for turning compiled LangGraph objects into Mermaid text and PNG files.
This module is mainly imported by lesson scripts, which call `build_and_save_mermaid(...)` in their `__main__` blocks.

## What It Actually Does

- Extracts Mermaid flowchart source from a compiled graph
- Saves Mermaid-rendered PNG files through LangGraph's Mermaid.INK-backed rendering
- Provides a reusable helper used by lesson scripts

## Key Functions

### `get_mermaid_for_graph(graph) -> str`

Calls:

```python
graph.get_graph().draw_mermaid()
```

If drawing fails, it returns a Mermaid-formatted error diagram string.

### `save_mermaid_png(graph, output_path: Path) -> bool`

Calls:

```python
graph.get_graph().draw_mermaid_png(max_retries=3, retry_delay=2)
```

and writes bytes to `output_path`.
Returns `True` on success, `False` on failure.

### `build_and_save_mermaid(name, graph, output_dir, print_mermaid=False, save_png=True) -> tuple[str, bool]`

- Builds Mermaid text
- Saves `<name>.png` under `output_dir` when `save_png=True`
- Optionally prints Mermaid text
- Returns `(mermaid_text, png_saved_ok)`

## About `main()`

`main()` currently prepares imports/output directory scaffolding but does not build lesson graphs or emit files by itself.
Practical usage is through imports from lesson files (for example `01_quickstart.py`, `02_persistence.py`, etc.).

## Usage Pattern

From lesson scripts:

```python
from utils.create_mermaid import build_and_save_mermaid
build_and_save_mermaid("graph_name", compiled_graph, output_dir)
```

## Requirements

- LangGraph installed
- Network access for PNG rendering (Mermaid.INK path used by `draw_mermaid_png`)
