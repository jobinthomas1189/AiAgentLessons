# 04_durable_execution.py

## Overview

LangGraph Durable Execution — Resumable workflows. Save progress at key points and resume after interruptions (e.g., crashes, restarts).

**Source:** [LangGraph Durable Execution](https://docs.langchain.com/oss/python/langgraph/durable-execution)

## Purpose

- **Durable execution:** Persist state so workflows can resume
- **`@task`:** Wrap side effects so they are not repeated on resume (memoization)
- **Determinism:** Non-deterministic code should live in tasks/nodes
- **Durability modes:** `sync`, `async`, `exit`

## Key Concepts

### Without `@task`

Side effects (e.g., API calls) run every time a node executes — including on resume. Risk of duplicate charges or duplicate actions.

### With `@task`

```python
@task
def _make_request(url: str):
    return f"[API result for {url}]"
```

- Result is cached per run
- On resume, the task returns the cached result instead of re-executing

### Durability Modes

| Mode | Behavior |
|------|----------|
| `sync` | Persist before each step (most durable) |
| `async` | Persist asynchronously (faster, small crash risk) |
| `exit` | Persist only on graph exit (fastest, no mid-run recovery) |

## Demos

### `demo_durable_execution()`

- Simple graph: `node_a` → `node_b`
- Uses `thread_id` for checkpointing
- Shows first run result and checkpoint state
- Explains durability modes

### `demo_task_wrapping()`

- Graph with `call_api_with_task` node
- Wraps API calls in `@task` for idempotency
- Invokes with multiple URLs; results are memoized

## Requirements

- `InMemorySaver` (checkpointer)
- `thread_id` in config (required for checkpointing)

## Usage

```bash
python 04_durable_execution.py
```
