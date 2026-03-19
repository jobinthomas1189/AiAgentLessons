# 05_supervisor_multi_agent.py

## Overview

Router-style multi-agent example using a supervisor node that sends input to one specialized agent.
Despite the filename using "supervisor", the implementation is a simple keyword router.

## State

```python
class MultiAgentState(TypedDict):
    messages: list
    routed_to: str | None
```

## Nodes

- `supervisor` (`router_node`): classifies latest user message
- `coding_agent`: returns coding-focused response text
- `math_agent`: returns calculation-focused response text
- `general_agent`: fallback response

## Routing Rules

- Contains `"python"` or `"code"` -> `coding_agent`
- Contains `"math"` or `"calculate"` -> `math_agent`
- Otherwise -> `general_agent`

## Graph Flow

```text
START -> supervisor -> (coding_agent | math_agent | general_agent) -> END
```

## Demo Behavior

`demo_router_pattern()` invokes the graph with three sample queries and prints:

- original query
- selected route (`routed_to`)
- final assistant message snippet

All invocations use the same thread id (`router-demo`) with `InMemorySaver`.

## Usage

```bash
python 05_supervisor_multi_agent.py
```

This script also exports a Mermaid diagram named `05_supervisor_multi_agent`.
