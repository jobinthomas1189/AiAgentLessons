"""
LangGraph Durable Execution - Resumable Workflows
Source: https://docs.langchain.com/oss/python/langgraph/durable-execution

Concepts:
- Durable execution: Save progress at key points, resume after interruptions
- @task: Wrap side effects so they're not repeated on resume
- thread_id: Required for checkpointing
- Determinism: Non-deterministic code should be in tasks/nodes
- Durability modes: sync, async, exit
"""

from typing import NotRequired
from typing_extensions import TypedDict
import uuid

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import task
from langgraph.graph import StateGraph, START, END
from pathlib import Path

# --- Without task: Side effect runs on every resume ---
class StateBasic(TypedDict):
    url: str
    result: NotRequired[str]


def call_api_basic(state: StateBasic):
    """Side effect (e.g., API call) runs every time node executes."""
    # Simulated API call - would run again on resume
    result = f"[API result for {state['url']}]"
    return {"result": result}


# --- With task: Side effect is memoized, not repeated on resume ---
class StateWithTask(TypedDict):
    urls: list[str]
    result: NotRequired[list[str]]


@task
def _make_request(url: str):
    """Side effect wrapped in task - result cached per run."""
    return f"[API result for {url}]"


def call_api_with_task(state: StateWithTask):
    """Uses tasks so API calls aren't repeated when resuming."""
    results = [_make_request(url) for url in state["urls"]]
    outputs = [r.result() for r in results]
    return {"result": outputs}


def _build_durable_execution_graph():
    class SimpleState(TypedDict):
        step: str
        count: int

    def node_a(state: SimpleState):
        return {"step": "a", "count": state.get("count", 0) + 1}

    def node_b(state: SimpleState):
        return {"step": "b", "count": state.get("count", 0) + 1}

    builder = StateGraph(SimpleState)
    builder.add_node("node_a", node_a)
    builder.add_node("node_b", node_b)
    builder.add_edge(START, "node_a")
    builder.add_edge("node_a", "node_b")
    builder.add_edge("node_b", END)
    return builder.compile(checkpointer=InMemorySaver())


def demo_durable_execution():
    """Demonstrate durable execution with checkpointer and thread_id."""
    print("=== Durable Execution ===\n")

    graph = _build_durable_execution_graph()

    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    # First run
    result1 = graph.invoke({"step": "", "count": 0}, config)
    print("First run:", result1)

    # Resume from same thread (e.g., after crash) - pass None as input
    # In a real scenario, you'd use: graph.invoke(None, config)
    # For demo, we show the checkpoint was saved
    snapshot = graph.get_state(config)
    print("Checkpoint saved:", snapshot.values)
    print()

    # --- Durability modes ---
    print("Durability modes: sync (default), async, exit")
    print("  sync: Persist before each step (most durable)")
    print("  async: Persist asynchronously (faster, small crash risk)")
    print("  exit: Persist only on graph exit (fastest, no mid-run recovery)")
    print()


def _build_task_wrapping_graph():
    builder = StateGraph(StateWithTask)
    builder.add_node("call_api", call_api_with_task)
    builder.add_edge(START, "call_api")
    builder.add_edge("call_api", END)
    return builder.compile(checkpointer=InMemorySaver())


def demo_task_wrapping():
    """Demonstrate wrapping side effects in @task."""
    print("=== Task Wrapping for Idempotency ===\n")

    graph = _build_task_wrapping_graph()

    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    result = graph.invoke(
        {"urls": ["https://example.com", "https://example.org"]},
        config,
    )
    print("Result with task-wrapped requests:", result)


if __name__ == "__main__":
    from utils.create_mermaid import build_and_save_mermaid

    output_dir = Path(__file__).resolve().parent.parent / "mermaids"
    output_dir.mkdir(parents=True, exist_ok=True)
    build_and_save_mermaid("04_durable_execution", _build_durable_execution_graph(), output_dir)
    build_and_save_mermaid("04_task_wrapping", _build_task_wrapping_graph(), output_dir)

    demo_durable_execution()
    demo_task_wrapping()
