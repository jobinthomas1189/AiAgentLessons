"""
LangChain Multi-Agent Patterns - Overview
Source: https://docs.langchain.com/oss/python/langchain/multi-agent

Patterns:
1. Subagents: Main agent coordinates subagents as tools
2. Handoffs: Tool calls update state → routing/configuration changes
3. Skills: Load specialized prompts/knowledge on-demand
4. Router: Classify input → route to specialized agents
5. Custom workflow: LangGraph with deterministic + agentic nodes

This script demonstrates a Router-style multi-agent pattern using LangGraph.
"""

from typing import Literal

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from typing_extensions import TypedDict
from pathlib import Path

# --- Shared state for multi-agent ---
class MultiAgentState(TypedDict):
    messages: list
    routed_to: str | None


def router_node(state: MultiAgentState):
    """Simple router: classify by keyword (in production, use LLM)."""
    last_msg = state["messages"][-1]["content"].lower()
    if "python" in last_msg or "code" in last_msg:
        return {"routed_to": "coding_agent"}
    if "math" in last_msg or "calculate" in last_msg:
        return {"routed_to": "math_agent"}
    return {"routed_to": "general_agent"}


def coding_agent_node(state: MultiAgentState):
    """Specialized agent for coding questions."""
    return {
        "messages": state["messages"]
        + [{"role": "assistant", "content": "[Coding Agent] Use Python best practices and type hints."}]
    }


def math_agent_node(state: MultiAgentState):
    """Specialized agent for math questions."""
    return {
        "messages": state["messages"]
        + [{"role": "assistant", "content": "[Math Agent] I'll help with calculations step by step."}]
    }


def general_agent_node(state: MultiAgentState):
    """General-purpose agent."""
    return {
        "messages": state["messages"]
        + [{"role": "assistant", "content": "[General Agent] How can I help you today?"}]
    }


def route_after_router(state: MultiAgentState) -> Literal["coding_agent", "math_agent", "general_agent"]:
    """Route to the appropriate agent based on router output."""
    return state.get("routed_to") or "general_agent"


def _build_router_graph():
    builder = StateGraph(MultiAgentState)
    builder.add_node("router", router_node)
    builder.add_node("coding_agent", coding_agent_node)
    builder.add_node("math_agent", math_agent_node)
    builder.add_node("general_agent", general_agent_node)

    builder.add_edge(START, "router")
    builder.add_conditional_edges(
        "router",
        route_after_router,
        ["coding_agent", "math_agent", "general_agent"],
    )
    builder.add_edge("coding_agent", END)
    builder.add_edge("math_agent", END)
    builder.add_edge("general_agent", END)
    return builder.compile(checkpointer=InMemorySaver())


def demo_router_pattern():
    """Router pattern: classify input, direct to one agent, synthesize."""
    print("=== Multi-Agent: Router Pattern ===\n")

    graph = _build_router_graph()

    # Test routing
    for query in ["Help me with Python code", "Calculate 2+2", "Hello!"]:
        result = graph.invoke(
            {"messages": [{"role": "user", "content": query}], "routed_to": None},
            config={"configurable": {"thread_id": "router-demo"}},
        )
        print(f"Query: {query}")
        print(f"  Routed to: {result['routed_to']}")
        print(f"  Response: {result['messages'][-1]['content'][:60]}...")
        print()


if __name__ == "__main__":
    from utils.create_mermaid import build_and_save_mermaid

    output_dir = Path(__file__).resolve().parent.parent / "mermaids"
    output_dir.mkdir(parents=True, exist_ok=True)
    build_and_save_mermaid("05_multi_agent", _build_router_graph(), output_dir)

    demo_router_pattern()
