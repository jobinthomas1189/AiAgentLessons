# 06_subgraphs.py

## Overview

LangGraph Subgraphs — Composing graphs. Use subgraphs as reusable building blocks inside parent graphs.

**Source:** [LangGraph Use Subgraphs](https://docs.langchain.com/oss/python/langgraph/use-subgraphs)

## Purpose

- **Pattern 1:** Call subgraph inside a node (different state schemas, transform I/O)
- **Pattern 2:** Add subgraph as a node (shared state keys, direct pass-through)
- **Streaming:** Use `subgraphs=True` with `stream_mode="updates"` (v2 format)

## Pattern 1: Call Subgraph Inside Node

### Different State Schemas

- **Parent state:** `foo: str`
- **Subgraph state:** `bar: str`, `baz: str`

### Flow

```
node_1 (parent) → call_subgraph (wrapper) → END
```

- `call_subgraph` transforms: `parent.foo` → subgraph input `{bar, baz}`
- Subgraph runs: `subgraph_node_1` → `subgraph_node_2`
- Output transformed back: `subgraph.bar` → `parent.foo`

### Code

```python
def call_subgraph(state: ParentState):
    subgraph_input = {"bar": state["foo"], "baz": ""}
    subgraph_output = subgraph.invoke(subgraph_input)
    return {"foo": subgraph_output["bar"]}
```

## Pattern 2: Add Subgraph as Node

### Shared State

- **SharedState:** `foo`, `bar` — both parent and subgraph use same keys

### Flow

```
node_1 (parent) → subgraph_shared (as node) → END
```

- Subgraph is added directly: `builder.add_node("node_2", subgraph_shared)`
- No wrapper; state passes through automatically

## Demos

- **`demo_call_subgraph_inside_node()`** — Pattern 1 with state transformation
- **`demo_add_subgraph_as_node()`** — Pattern 2 with shared state
- **`demo_stream_subgraphs()`** — Streaming with `subgraphs=True`, v2 format

## Subgraph Persistence Options

- **Per-invocation** (default) — Fresh state each call
- **Per-thread** — Persist across invocations in same thread
- **Stateless** — No persistence

## Usage

```bash
python 06_subgraphs.py
```
