# 06_subgraphs_multi_agent.py

## Overview

Subgraph composition examples in two concrete styles:

1. invoke a subgraph from inside a parent node (different schemas)
2. attach a compiled subgraph directly as a parent node (shared schema)

## Pattern 1: Subgraph Called Inside Node

### Schemas

- Parent: `ParentState` with `foo`
- Subgraph: `SubgraphState` with `bar`, `baz`

### Behavior

- Parent `node_1` prefixes `foo` with `"hi! "`
- `call_subgraph` maps `foo -> bar`, invokes subgraph, maps output back to `foo`
- Subgraph internal flow:
  - `subgraph_node_1` sets `baz = "baz"`
  - `subgraph_node_2` sets `bar = bar + baz`

### Parent Flow

```text
START -> node_1 -> node_2(call_subgraph) -> END
```

## Pattern 2: Subgraph Added As Node

### Shared Schema

Both parent and subgraph use:

```python
class SharedState(TypedDict):
    foo: str
    bar: str
```

### Behavior

- Parent `node_1` prefixes `foo`
- `node_2` is the compiled subgraph itself
- Shared keys pass through directly without wrapper mapping

### Parent Flow

```text
START -> node_1 -> node_2(subgraph_shared) -> END
```

## Demo Functions

- `demo_call_subgraph_inside_node()`
- `demo_add_subgraph_as_node()`

## Usage

```bash
python 06_subgraphs_multi_agent.py
```

Running the file exports Mermaid diagrams for both parent graph variants.
