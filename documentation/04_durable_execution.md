# 04_durable_execution.py

## Overview

Durable execution demonstration focused on two things:

- checkpoint-backed graph recovery with `thread_id`
- idempotent side effects using `@task`

## Main Pieces

### 1) Basic durable graph

- Internal state: `step`, `count`
- Flow: `START -> node_a -> node_b -> END`
- Compiled with `InMemorySaver`
- Demo shows:
  - first invocation result
  - checkpoint retrieval via `graph.get_state(config)`
  - durability mode explanations (`sync`, `async`, `exit`)

### 2) Task-wrapped side effects

```python
@task
def _make_request(url: str):
    return f"[API result for {url}]"
```

- `call_api_with_task` executes requests through task futures
- `.result()` resolves each task output
- Intended to avoid repeating side effects on resume

## Included State Types

- `StateBasic`: single URL example without task wrapping
- `StateWithTask`: list-of-URLs example with task wrapping

## Demo Functions

- `demo_durable_execution()`: checkpoint behavior and durability mode notes
- `demo_task_wrapping()`: task-based request execution demo

## Usage

```bash
python 04_durable_execution.py
```

Running the file also exports Mermaid diagrams for both compiled graphs.
