# LangGraph Server Setup

This guide explains how to run the local LangGraph server for the calculator graph in `agentic_files/server_graph.py`.

## Prerequisites

- Python 3.12+
- Virtual environment created in project root
- Dependencies installed from `agentic_files/requirements.txt`

## Quick setup

From `AiAgentLessons`:

```bash
python3.12 -m venv aienv
source aienv/bin/activate
pip install -r agentic_files/requirements.txt
cp agentic_files/.env.example agentic_files/.env
```

Then edit `agentic_files/.env` and set:

```bash
ANTHROPIC_API_KEY=your_key_here
```

## Environment variables (the `.env` file)

LangGraph dev server loads environment variables from:

- `agentic_files/.env` (configured in root `langgraph.json`)

Create it from the example file:

```bash
cp agentic_files/.env.example agentic_files/.env
```

### Required

- `ANTHROPIC_API_KEY`: required for this graph because it calls Anthropic Claude via `init_chat_model(...)`.

### Optional (LangSmith tracing)

If you want request/trace logging in LangSmith, set:

```bash
LANGSMITH_API_KEY=your_key_here
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=AiAgentLessons
```

## Run the server

From `AiAgentLessons`:

```bash
langgraph dev
```

## URLs

- API: `http://localhost:2024`
- Docs: `http://localhost:2024/docs`
- Studio: opens automatically in browser

## Why this now works from project root

The project includes a root-level `langgraph.json` that points to:

- Graph: `./agentic_files/server_graph.py:graph`
- Env file: `./agentic_files/.env`

So you can run `langgraph dev` directly from `AiAgentLessons` without changing directories.

## Common issue

If you see:

```text
Error: Invalid value for '--config': Path 'langgraph.json' does not exist.
```

you are in a directory that does not contain `langgraph.json`. Fix by:

- running the command from `AiAgentLessons`, or
- passing an explicit config path:

```bash
langgraph dev --config /full/path/to/AiAgentLessons/langgraph.json
```

If you see:

```text
Error: Required package 'langgraph-api' is not installed.
```

install the in-memory dev dependencies:

```bash
source aienv/bin/activate
pip install -U "langgraph-cli[inmem]"
```
