# 07_handoffs.py

## Overview

LangChain Multi-Agent Handoffs. Agents transfer control to each other based on user intent. State-driven behavior: `active_agent` determines which agent handles the next turn.

**Source:** [LangChain Multi-Agent Handoffs](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs)

## Purpose

- **Handoffs:** Tools or logic update `active_agent` → routing changes
- **Multiple agent subgraphs:** Sales and Support as distinct nodes
- **Conditional routing:** Route based on `active_agent` after each turn

## Key Concepts

### Handoff Mechanism

1. Agent detects need to transfer (e.g., "login" → support, "buy" → sales)
2. Agent updates `active_agent` in state
3. Conditional edges route to the new agent on next step

### State

```python
class HandoffState(TypedDict):
    messages: list
    active_agent: NotRequired[str]  # "sales_agent" | "support_agent"
```

## Graph Flow

```
START → (sales_agent | support_agent)  [route_initial]
sales_agent  → (sales_agent | support_agent | END)  [route_after_agent]
support_agent → (sales_agent | support_agent | END)  [route_after_agent]
```

## Nodes

| Node | Role |
|------|------|
| `sales_agent_node` | Handles pricing/purchasing; hands off to support on "login", "broken", "support" |
| `support_agent_node` | Handles technical issues; hands off to sales on "buy", "price", "sales" |

## Routing Logic

- **`route_initial`:** Default to `sales_agent` (or use `active_agent` if set)
- **`route_after_agent`:** If last message contains "Transferring", route to `active_agent`; else `END`

## Demo

`demo_handoffs()` — User says "My account login is broken":

1. Starts with sales (default)
2. Sales detects "login" → sets `active_agent: "support_agent"`
3. Routes to support for next turn
4. Support responds with technical help

## Usage

```bash
python 07_handoffs.py
```
