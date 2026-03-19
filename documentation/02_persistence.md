# 02_persistence.py

## Overview

Persistence walkthrough for LangGraph checkpointing using `InMemorySaver`.
The script demonstrates how thread-scoped state snapshots are created, inspected, filtered, and manually updated.

## Core State and Graph

```python
class State(TypedDict):
    foo: str
    bar: Annotated[list[str], add]
```

- Reducer `add` appends values into `bar` across node updates
- Main flow: `START -> node_a -> node_b -> END`
- Compiled with `checkpointer=InMemorySaver()`

## What Each Demo Shows

### `demo_checkpoints()`

- Invokes graph with `thread_id="1"`
- Reads latest snapshot with `graph.get_state(config)`
- Prints key metadata (`values`, `next`, `step`)
- Iterates `graph.get_state_history(config)` to inspect recent checkpoints

### `demo_update_state()`

- Runs a smaller one-node graph
- Calls `graph.update_state(config, {...})`
- Shows manual updates create a new checkpoint rather than mutating history

### `demo_filter_history()`

- Loads history list from one thread
- Finds targeted checkpoints with:
  - `next == ("node_b",)`
  - `metadata["step"] == 2`

## Helper Functions

- `_build_persistence_graph()`: returns compiled `node_a -> node_b` graph
- `get_graphs_for_mermaid()`: provides named graph tuple for diagram export

## Usage

```bash
python 02_persistence.py
```

Running the file exports Mermaid output and executes all three persistence demos.
