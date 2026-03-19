# 01_quickstart.py

## Overview

Quickstart calculator agent showing the same behavior implemented with:

- Graph API (`StateGraph`)
- Functional API (`@entrypoint` + `@task`)

## What The Script Contains

- Tool definitions: `add`, `multiply`, `divide`
- Model setup with tool binding (`claude-sonnet-4-6`, temperature `0`)
- Graph API implementation with explicit nodes and edges
- Functional API implementation with loop-based control flow
- Mermaid export for the Graph API workflow

## Graph API Details

### State

```python
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int
```

### Nodes

- `llm_call`: sends system prompt + history to model, increments `llm_calls`
- `tool_node`: executes each tool call and returns `ToolMessage` responses
- `should_continue`: routes to tools if present, otherwise ends

### Flow

```text
START -> llm_call -> (tool_node or END)
          ^              |
          |______________|
```

## Functional API Details

- `call_llm` task: requests next model step
- `call_tool` task: runs one tool call
- `functional_agent` entrypoint:
  - call model
  - if tool calls exist, execute tools and append results
  - repeat until no tool calls remain

## Demo Functions

- `run_graph_api_example()`: one-shot invoke, then pretty-prints message trace
- `run_functional_api_example()`: streams incremental updates

## Usage

```bash
python 01_quickstart.py
```

Running the file exports a Mermaid diagram and executes both demos.
