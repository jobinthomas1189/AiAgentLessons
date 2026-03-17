# 02_persistence.py

## Overview

LangGraph Persistence — Checkpointing and state management. Covers threads, checkpoints, `get_state()`, `get_state_history()`, and `update_state()`.

**Source:** [LangGraph Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

## Purpose

- Explain **threads** (unique IDs for checkpoint storage)
- Show **checkpoints** (state snapshots at each super-step)
- Demonstrate `get_state()`, `get_state_history()`, and `update_state()`
- Use `InMemorySaver` for development

## Key Concepts

### State

```python
class State(TypedDict):
    foo: str
    bar: Annotated[list[str], add]  # Reducer: append
```

### Graph Flow

```
START → node_a → node_b → END
```

- `node_a`: sets `foo="a"`, `bar=["a"]`
- `node_b`: sets `foo="b"`, `bar=["b"]`

## Demo Functions

### `demo_checkpoints()`

- Runs graph with `thread_id: "1"`
- Shows `get_state(config)` — latest snapshot (values, next, metadata)
- Shows `get_state_history(config)` — chronological history of checkpoints

### `demo_update_state()`

- Runs graph, then calls `update_state(config, {...})`
- Demonstrates manual state override (creates new checkpoint)

### `demo_filter_history()`

- Filters history by `next == ("node_b",)` or `metadata.step == 2`
- Shows querying specific checkpoints

## Key APIs

| API | Purpose |
|-----|---------|
| `graph.get_state(config)` | Latest state snapshot |
| `graph.get_state_history(config)` | Iterator over all checkpoints |
| `graph.update_state(config, values)` | Manually update state (new checkpoint) |

## Usage

```bash
python 02_persistence.py
```
