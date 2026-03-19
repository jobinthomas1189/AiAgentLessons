# 07_handoffs_multi_agent.py

## Overview

Two-agent handoff workflow where Sales and Support transfer control using tool-driven `Command` objects.
The active route is tracked in state via `active_agent`.

## State

```python
class HandoffState(TypedDict):
    messages: list[AnyMessage]
    active_agent: NotRequired[str]
```

## Transfer Tools

- `transfer_to_support(tool_call_id)`:
  - returns `Command(goto="support_agent", update={...})`
  - appends a `ToolMessage("Transferred to support agent")`
- `transfer_to_sales(tool_call_id)`:
  - returns `Command(goto="sales_agent", update={...})`
  - appends a `ToolMessage("Transferred to sales agent")`

## Agent Logic

- `sales_agent_node`:
  - if last message mentions `login`, `broken`, or `support`, it creates a tool call and hands off to support
  - otherwise returns a sales response
- `support_agent_node`:
  - if last message mentions `buy`, `price`, or `sales`, it hands off to sales
  - otherwise returns a support response

## Routing

```text
START -> route_initial -> sales_agent|support_agent
sales_agent -> route_after_agent -> sales_agent|support_agent|END
support_agent -> route_after_agent -> sales_agent|support_agent|END
```

- `route_initial`: defaults to `sales_agent` if `active_agent` is unset
- `route_after_agent`: continues only when the last message is a `ToolMessage`; otherwise ends

## Demo

`demo_handoffs()` runs one scenario: user reports login trouble.
Because the initial route is sales, Sales immediately performs a handoff to Support.

## Usage

```bash
python 07_handoffs_multi_agent.py
```

The script exports a Mermaid diagram named `07_handoffs_multi_agent`.
