# 05_multi_agent.py

## Overview

LangChain Multi-Agent Patterns — Router pattern. Classify input and route to specialized agents (coding, math, general).

**Source:** [LangChain Multi-Agent](https://docs.langchain.com/oss/python/langchain/multi-agent)

## Purpose

Demonstrates the **Router** multi-agent pattern:

1. **Router** — Classify user input
2. **Specialized agents** — `coding_agent`, `math_agent`, `general_agent`
3. **Conditional routing** — Route to one agent based on classification

## Other Patterns (Overview)

- **Subagents** — Main agent coordinates subagents as tools
- **Handoffs** — Tool calls update state → routing changes (see `07_handoffs.py`)
- **Skills** — Load specialized prompts/knowledge on-demand
- **Custom workflow** — LangGraph with deterministic + agentic nodes

## Graph Flow

```
START → router → (coding_agent | math_agent | general_agent) → END
```

## State

```python
class MultiAgentState(TypedDict):
    messages: list
    routed_to: str | None
```

## Nodes

| Node | Role |
|------|------|
| `router_node` | Keyword-based routing (production: use LLM) |
| `coding_agent_node` | Handles Python/code questions |
| `math_agent_node` | Handles math/calculation questions |
| `general_agent_node` | General-purpose fallback |

## Routing Logic

- `"python"` or `"code"` → `coding_agent`
- `"math"` or `"calculate"` → `math_agent`
- Default → `general_agent`

## Demo

`demo_router_pattern()` runs three test queries:

- "Help me with Python code" → coding_agent
- "Calculate 2+2" → math_agent
- "Hello!" → general_agent

## Usage

```bash
python 05_multi_agent.py
```
