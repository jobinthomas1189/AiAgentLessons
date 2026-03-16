"""
LangGraph Subgraphs - Composing Graphs
Source: https://docs.langchain.com/oss/python/langgraph/use-subgraphs

Concepts:
1. Call subgraph inside a node: Different state schemas, transform I/O
2. Add subgraph as a node: Shared state keys, direct pass-through
3. Subgraph persistence: per-invocation (default), per-thread, stateless
4. Streaming with subgraphs=True
"""

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


# --- Pattern 1: Call subgraph inside a node (different state schemas) ---
class SubgraphState(TypedDict):
    bar: str
    baz: str


class ParentState(TypedDict):
    foo: str


def subgraph_node_1(state: SubgraphState):
    return {"baz": "baz"}


def subgraph_node_2(state: SubgraphState):
    return {"bar": state["bar"] + state["baz"]}


# Build subgraph (call_subgraph references this)
subgraph_builder = StateGraph(SubgraphState)
subgraph_builder.add_node("subgraph_node_1", subgraph_node_1)
subgraph_builder.add_node("subgraph_node_2", subgraph_node_2)
subgraph_builder.add_edge(START, "subgraph_node_1")
subgraph_builder.add_edge("subgraph_node_1", "subgraph_node_2")
subgraph_builder.add_edge("subgraph_node_2", END)
subgraph = subgraph_builder.compile()


def call_subgraph(state: ParentState):
    """Transform parent state -> subgraph input, subgraph output -> parent."""
    subgraph_input = {"bar": state["foo"], "baz": ""}
    subgraph_output = subgraph.invoke(subgraph_input)
    return {"foo": subgraph_output["bar"]}


def node_1(state: ParentState):
    return {"foo": "hi! " + state["foo"]}


def demo_call_subgraph_inside_node():
    """Subgraph with different state - invoked inside a wrapper node."""
    print("=== Call Subgraph Inside Node (Different State) ===\n")

    builder = StateGraph(ParentState)
    builder.add_node("node_1", node_1)
    builder.add_node("node_2", call_subgraph)
    builder.add_edge(START, "node_1")
    builder.add_edge("node_1", "node_2")
    builder.add_edge("node_2", END)
    graph = builder.compile()

    result = graph.invoke({"foo": "foo"})
    print("Result:", result)
    print()


# --- Pattern 2: Add subgraph as a node (shared state) ---
class SharedState(TypedDict):
    foo: str
    bar: str


def subgraph_shared_node_1(state: SharedState):
    return {"bar": "bar"}


def subgraph_shared_node_2(state: SharedState):
    return {"foo": state["foo"] + state["bar"]}


def parent_node_1(state: SharedState):
    return {"foo": "hi! " + state["foo"]}


def demo_add_subgraph_as_node():
    """Subgraph with shared state - added directly as node."""
    print("=== Add Subgraph as Node (Shared State) ===\n")

    subgraph_shared_builder = StateGraph(SharedState)
    subgraph_shared_builder.add_node("sg_1", subgraph_shared_node_1)
    subgraph_shared_builder.add_node("sg_2", subgraph_shared_node_2)
    subgraph_shared_builder.add_edge(START, "sg_1")
    subgraph_shared_builder.add_edge("sg_1", "sg_2")
    subgraph_shared_builder.add_edge("sg_2", END)
    subgraph_shared = subgraph_shared_builder.compile()

    builder = StateGraph(SharedState)
    builder.add_node("node_1", parent_node_1)
    builder.add_node("node_2", subgraph_shared)  # Subgraph as node
    builder.add_edge(START, "node_1")
    builder.add_edge("node_1", "node_2")
    builder.add_edge("node_2", END)
    graph = builder.compile()

    result = graph.invoke({"foo": "foo", "bar": ""})
    print("Result:", result)
    print()


# --- Stream with subgraphs ---
def demo_stream_subgraphs():
    """Stream updates including subgraph nodes."""
    print("=== Stream with subgraphs=True (v2 stream format) ===\n")

    builder = StateGraph(ParentState)
    builder.add_node("node_1", node_1)
    builder.add_node("node_2", call_subgraph)
    builder.add_edge(START, "node_1")
    builder.add_edge("node_1", "node_2")
    builder.add_edge("node_2", END)
    graph = builder.compile()

    print("Stream chunks:")
    for chunk in graph.stream(
        {"foo": "foo"},
        stream_mode="updates",
        subgraphs=True,
        version="v2",
    ):
        if chunk["type"] == "updates":
            print("  ns:", chunk["ns"], "data:", chunk["data"])


if __name__ == "__main__":
    demo_call_subgraph_inside_node()
    demo_add_subgraph_as_node()
    demo_stream_subgraphs()
