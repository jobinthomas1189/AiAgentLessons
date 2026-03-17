# server_graph.py

## Overview

Server-ready LangGraph for the LangGraph dev server. Exports a calculator agent compiled with checkpointing for use with `langgraph.json`.

## Purpose

- Provides a **production-ready graph** that the LangGraph dev server can load
- Same logic as `01_quickstart.py` but compiled with `InMemorySaver` for persistence
- Exported as `graph` for `langgraph.json` configuration

## Key Components

### Tools

- **`multiply(a, b)`** — Multiplies two integers
- **`add(a, b)`** — Adds two integers
- **`divide(a, b)`** — Divides two numbers (returns float)

### State

- **`MessagesState`** — TypedDict with `messages` (annotated with `operator.add` for message accumulation)

### Nodes

- **`llm_call`** — Invokes the LLM with system prompt and message history; decides whether to call tools
- **`tool_node`** — Executes tool calls from the LLM and returns `ToolMessage` results

### Flow

1. `START` → `llm_call`
2. `llm_call` → conditional: `tool_node` (if tool calls) or `END`
3. `tool_node` → `llm_call` (loop until no more tool calls)

## Dependencies

- `langchain` (tools, chat models, messages)
- `langgraph` (StateGraph, checkpointer)
- `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` for `init_chat_model`

## Usage

Used by the LangGraph dev server via `langgraph.json`. The graph is imported as `graph` and served as an API.
