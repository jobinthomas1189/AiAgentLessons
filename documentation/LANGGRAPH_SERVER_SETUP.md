# LangGraph Server Setup

This guide explains how to run the local LangGraph dev server from the project root.
Current server config is in `langgraph.json`.

## Current Config (Important)

The root `langgraph.json` currently contains:

- `graphs.calculator = ./agentic_files/server_graph_registry.py:graph_00_server_graph`
- `env = .env`
- `dependencies = ["./agentic_files"]`

So by default, the served graph is lesson `00` through the registry export.

## Prerequisites

- Python 3.12+
- Virtual environment in project root
- Dependencies installed from `agentic_files/requirements.txt`

## Quick Setup

From `AiAgentLessons`:

```bash
python3.12 -m venv aienv
source aienv/bin/activate
pip install -r agentic_files/requirements.txt
cp agentic_files/.env.example .env
```

Then edit root `.env` and set keys as needed.

## Environment Variables

The dev server loads env vars from root `.env` (not `agentic_files/.env`).

Example values from `agentic_files/.env.example`:

```bash
OPENAI_API_KEY=your_openai_key
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=AiAgentLessons
```

## Run The Server

From `AiAgentLessons`:

```bash
langgraph dev
```

Or use the helper script to choose graph index `0-7` and update `langgraph.json` automatically:

```bash
./run_langgraph_server.sh 0
```

Set config without starting server:

```bash
./run_langgraph_server.sh 0 --set-only
```

## URLs

- API: `http://localhost:2024`
- Docs: `http://localhost:2024/docs`
- Studio: URL appears in terminal when server starts

## Common Issues

If you see:

```text
Error: Invalid value for '--config': Path 'langgraph.json' does not exist.
```

Run from `AiAgentLessons`, or pass explicit config path:

```bash
langgraph dev --config /full/path/to/AiAgentLessons/langgraph.json
```

If you see:

```text
Error: Required package 'langgraph-api' is not installed.
```

Install CLI in-memory extras:

```bash
source aienv/bin/activate
pip install -U "langgraph-cli[inmem]"
```
