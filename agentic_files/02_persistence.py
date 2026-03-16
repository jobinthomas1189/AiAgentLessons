"""
LangGraph Persistence - Checkpointing & State
Source: https://docs.langchain.com/oss/python/langgraph/persistence

Concepts:
- Threads: Unique ID for checkpoint storage (thread_id)
- Checkpoints: State snapshot at each super-step
- get_state() / get_state_history()
- update_state()
- InMemorySaver for development
"""

from typing import Annotated
from typing_extensions import TypedDict
from operator import add

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END


# --- Define state with reducer ---
class State(TypedDict):
    foo: str
    bar: Annotated[list[str], add]


def node_a(state: State):
    return {"foo": "a", "bar": ["a"]}


def node_b(state: State):
    return {"foo": "b", "bar": ["b"]}


def demo_checkpoints():
    """Show checkpoints saved at each super-step."""
    print("=== Persistence: Checkpoints & Threads ===\n")

    workflow = StateGraph(State)
    workflow.add_node("node_a", node_a)
    workflow.add_node("node_b", node_b)
    workflow.add_edge(START, "node_a")
    workflow.add_edge("node_a", "node_b")
    workflow.add_edge("node_b", END)

    checkpointer = InMemorySaver()
    graph = workflow.compile(checkpointer=checkpointer)

    config = {"configurable": {"thread_id": "1"}}
    graph.invoke({"foo": "", "bar": []}, config)

    # Get latest state
    snapshot = graph.get_state(config)
    print("Latest state (get_state):")
    print("  values:", snapshot.values)
    print("  next:", snapshot.next)
    print("  metadata step:", snapshot.metadata.get("step"))
    print()

    # Get full history
    history = list(graph.get_state_history(config))
    print("State history (chronological, most recent first):")
    for i, s in enumerate(history[:3]):
        print(f"  [{i}] step={s.metadata.get('step')}, next={s.next}, values={s.values}")
    print()


def demo_update_state():
    """Update state manually - creates new checkpoint."""
    print("=== Update State ===\n")

    workflow = StateGraph(State)
    workflow.add_node("node_a", node_a)
    workflow.add_edge(START, "node_a")
    workflow.add_edge("node_a", END)
    checkpointer = InMemorySaver()
    graph = workflow.compile(checkpointer=checkpointer)

    config = {"configurable": {"thread_id": "update-demo"}}
    graph.invoke({"foo": "", "bar": []}, config)
    print("After invoke:", graph.get_state(config).values)

    # Update state (creates new checkpoint, doesn't modify original)
    graph.update_state(config, {"foo": "manual_override", "bar": ["extra"]})
    print("After update_state:", graph.get_state(config).values)
    print()


def demo_filter_history():
    """Filter state history by criteria."""
    print("=== Filter State History ===\n")

    workflow = StateGraph(State)
    workflow.add_node("node_a", node_a)
    workflow.add_node("node_b", node_b)
    workflow.add_edge(START, "node_a")
    workflow.add_edge("node_a", "node_b")
    workflow.add_edge("node_b", END)
    checkpointer = InMemorySaver()
    graph = workflow.compile(checkpointer=checkpointer)

    config = {"configurable": {"thread_id": "filter-demo"}}
    graph.invoke({"foo": "", "bar": []}, config)

    history = list(graph.get_state_history(config))
    before_node_b = next(s for s in history if s.next == ("node_b",))
    step_2 = next(s for s in history if s.metadata.get("step") == 2)
    print("Checkpoint before node_b:", before_node_b.values)
    print("Checkpoint at step 2:", step_2.values)


if __name__ == "__main__":
    demo_checkpoints()
    demo_update_state()
    demo_filter_history()
