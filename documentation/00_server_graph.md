# 00_server_graph.py

## Overview

Server-ready LangGraph calculator graph exported as `graph` for LangGraph API runtime.
This file is the deployment-friendly version of the calculator flow used in quickstart examples.

## What It Builds

- Arithmetic tools: `add`, `multiply`, `divide`
- A tool-enabled chat model (`gpt-5.4`)
- A `StateGraph` with message accumulation
- Conditional loop: LLM decides tool calls, tool results return to LLM, then finish

## State

```python
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
```

The reducer `operator.add` appends new messages each step.

## Graph Flow

```text
START -> llm_call -> (tool_node or END)
          ^              |
          |______________|
```

- `llm_call`: runs model with system prompt plus current conversation
- `tool_node`: executes each requested tool call and returns `ToolMessage` objects
- `should_continue`: routes to `tool_node` if the latest AI message has tool calls, else `END`

## Runtime Notes

- Loads local `.env` from the same directory for direct execution/import use
- Exports compiled graph as top-level variable `graph` for server discovery
- Includes one inline example input payload in the script as a reference object literal

## Usage

Used by LangGraph server configuration (via `langgraph.json`) rather than as a standalone CLI demo.
