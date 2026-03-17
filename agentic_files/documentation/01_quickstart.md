# 01_quickstart.py

## Overview

LangGraph Quickstart — Calculator Agent. Demonstrates two ways to build an agent: **Graph API** and **Functional API**.

**Source:** [LangGraph Quickstart](https://docs.langchain.com/oss/python/langgraph/quickstart)

## Purpose

- Introduce LangGraph basics with a simple arithmetic calculator agent
- Compare **Graph API** (nodes + edges) vs **Functional API** (control flow with `@task` and `@entrypoint`)

## Key Concepts

### Graph API

1. **Tools** — `add`, `multiply`, `divide` (LangChain `@tool`)
2. **State** — `MessagesState` with `messages` and `llm_calls`
3. **Nodes** — `llm_call` (LLM decides tool usage), `tool_node` (executes tools)
4. **Edges** — Conditional: `llm_call` → `tool_node` or `END`; `tool_node` → `llm_call`

### Functional API

- Uses `@task` for async/cached steps (`call_llm`, `call_tool`)
- Uses `@entrypoint()` for the main agent function
- Control flow: `call_llm` → loop over tool calls → `call_tool` → `call_llm` until done

## Flow (Graph API)

```
START → llm_call → (tool_node or END)
         ↑              |
         └──────────────┘
```

## Demo Functions

- **`run_graph_api_example()`** — Invokes Graph API agent with "Add 3 and 4."
- **`run_functional_api_example()`** — Streams Functional API agent output

## Requirements

- `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`
- `init_chat_model("claude-sonnet-4-6", temperature=0)`

## Usage

```bash
python 01_quickstart.py
```

Runs both demos: Graph API and Functional API.
