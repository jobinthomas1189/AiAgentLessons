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

| File | Concept | Source |
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
