# LangGraph Lesson Mapping

This document explains why each demo script in this repository is the "right" lesson for its corresponding LangGraph concept, as outlined in the official documentation.

## 1. Quickstart (`01_quickstart.py`)

**Doc:** [Quickstart](https://docs.langchain.com/oss/python/langgraph/quickstart)

- **The Lesson:** Teaches the fundamental shift from linear chains to **cyclic graphs**.
- **Why it's right:** It introduces the `StateGraph`, `nodes`, and `edges`. By using a simple calculator agent, it demonstrates how an agent can "loop" back to a tool-calling node until it has the final answer, which is the core value proposition of LangGraph over standard LangChain.

## 2. Persistence (`02_persistence.py`)

**Doc:** [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

- **The Lesson:** Teaches how to give agents **long-term memory** and "time-travel" capabilities.
- **Why it's right:** It introduces `checkpointers` and `thread_id`. The demo shows that by simply providing a thread ID, the agent remembers previous interactions. It also covers `get_state` and `update_state`, which are essential for debugging and manual state intervention.

## 3. Interrupts (`03_interrupts.py`)

**Doc:** [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)

- **The Lesson:** Teaches **Human-in-the-loop (HITL)** patterns.
- **Why it's right:** It demonstrates how to pause execution before sensitive actions (like tool calls) using `interrupt()`. This is the "right" lesson because it shows how to build safe, controllable agents that don't just run autonomously but can wait for human approval or input.

## 4. Durable Execution (`04_durable_execution.py`)

**Doc:** [Durable Execution](https://docs.langchain.com/oss/python/langgraph/durable-execution)

- **The Lesson:** Teaches **fault-tolerance** and the `@task` decorator.
- **Why it's right:** It explains how LangGraph ensures that if a process crashes, it can resume from the exact point of failure. The demo uses the Functional API style to show how individual tasks are checkpointed, making the workflow "durable" across restarts.

## 5. Subgraphs (`05_subgraphs.py`)

**Doc:** [Use Subgraphs](https://docs.langchain.com/oss/python/langgraph/use-subgraphs)

- **The Lesson:** Teaches **modularity** and hierarchical state management.
- **Why it's right:** It shows two patterns: calling a subgraph inside a node (encapsulation) vs. adding a subgraph as a node (shared state). This is crucial for building complex systems where you want to isolate the logic of a specific "specialist" agent from the main "manager" graph.

## 6. Multi-Agent Systems (`06_multi_agent.py`)

**Doc:** [Multi-Agent](https://docs.langchain.com/oss/python/langchain/multi-agent)

- **The Lesson:** Teaches the **Router** pattern for multi-agent collaboration.
- **Why it's right:** It demonstrates a "Manager" or "Router" that decides which specialist agent to call next. This is the foundational multi-agent pattern where agents communicate via a shared state, allowing for complex, multi-step problem solving that a single agent couldn't handle.

## 7. Handoffs (`07_handoffs.py`)

**Doc:** [Handoffs](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs)

- **The Lesson:** Teaches **explicit state-driven routing** between agents.
- **Why it's right:** Unlike the general multi-agent router, handoffs are about one agent explicitly "passing the baton" to another (e.g., Sales to Support). The demo shows how to use the graph state to trigger these transitions, which is the standard way to implement structured workflows between different personas.

