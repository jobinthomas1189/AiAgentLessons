# AiAgentLessons – LangGraph & Multi-Agent Concepts

Python scripts demonstrating LangChain/LangGraph concepts, based on the official documentation.

## Explain Aux links and materials

## Explain the 3 directories
## Setup

```bash
python3.12 -m venv aienv
source aienv/bin/activate
pip install -r agentic_files/requirements.txt
python {agentic_file}
```

For `01_quickstart.py`, set `ANTHROPIC_API_KEY` (or use another model via `init_chat_model`).

## Scripts

| File | Concept | Langgraph Doc |
|------|---------|--------|
| `01_quickstart.py` | Calculator agent with **Graph API** and **Functional API** | [quickstart](https://docs.langchain.com/oss/python/langgraph/quickstart) |
| `02_persistence.py` | Checkpointing, **threads**, `get_state`, `update_state`, history | [persistence](https://docs.langchain.com/oss/python/langgraph/persistence) |
| `03_interrupts.py` | Human-in-the-loop with `interrupt()`, `Command(resume=...)`, approval flows | [interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) |
| `04_durable_execution.py` | Durable execution, `@task`, resumable workflows, durability modes | [durable-execution](https://docs.langchain.com/oss/python/langgraph/durable-execution) |
| `05_subgraphs.py` | Subgraphs: call inside node vs add as node, streaming, persistence modes | [use-subgraphs](https://docs.langchain.com/oss/python/langgraph/use-subgraphs) |
| `06_multi_agent.py` | Router-style multi-agent pattern | [multi-agent](https://docs.langchain.com/oss/python/langchain/multi-agent) |
| `07_handoffs.py` | Agent handoffs via state-driven routing (sales ↔ support) | [handoffs](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs) |

## Run

```bash
# All scripts except 01 work without API keys
python 02_persistence.py
python 03_interrupts.py
python 04_durable_execution.py
python 05_subgraphs.py
python 06_multi_agent.py
python 07_handoffs.py

# 01 requires ANTHROPIC_API_KEY
python 01_quickstart.py
```

## LangGraph Server

Run the calculator agent as a local API server with LangGraph Studio:

Detailed setup guide: [`LANGGRAPH_SERVER_SETUP.md`](./LANGGRAPH_SERVER_SETUP.md)

```bash
cp agentic_files/.env.example agentic_files/.env   # Edit and add ANTHROPIC_API_KEY (required)
pip install -r agentic_files/requirements.txt
langgraph dev
```

- **API**: http://localhost:2024
- **Docs**: http://localhost:2024/docs
- **Studio**: Opens in browser for visualization and debugging

Test with the SDK:

```python
from langgraph_sdk import get_sync_client

client = get_sync_client(url="http://localhost:2024")
for chunk in client.runs.stream(
    None,
    "calculator",
    input={"messages": [{"role": "human", "content": "Add 3 and 4."}]},
    stream_mode="messages-tuple",
):
    print(chunk)
```

## LangSmith Tracing

Set `LANGSMITH_API_KEY` in `.env` to trace runs in [LangSmith](https://smith.langchain.com/). Get a free API key at [smith.langchain.com/settings](https://smith.langchain.com/settings).
