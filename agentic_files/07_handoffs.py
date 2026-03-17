"""
LangChain Multi-Agent Handoffs
Source: https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs

Concepts:
- Handoffs: Tools update state variable (e.g. active_agent) → behavior changes
- Single agent with middleware: Dynamic config (prompt, tools) per step
- Multiple agent subgraphs: Distinct agents as nodes, handoff tools with Command

This script demonstrates handoffs using StateGraph with conditional routing.
State-driven behavior: active_agent determines which agent handles the next turn.
"""

from typing import Literal

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from typing_extensions import NotRequired, TypedDict
from pathlib import Path

# --- Multiple agent subgraphs pattern ---
class HandoffState(TypedDict):
    messages: list
    active_agent: NotRequired[str]


def sales_agent_node(state: HandoffState):
    """Sales agent - can hand off to support."""
    # In full impl: LLM call with transfer_to_support tool
    # Tool updates active_agent -> "support_agent"
    msgs = state.get("messages", [])
    last = msgs[-1] if msgs else {}
    content = (last.get("content") or "").lower()
    if "login" in content or "broken" in content or "support" in content:
        # Simulate handoff: would be triggered by tool call in real impl
        return {
            "messages": msgs
            + [
                {
                    "role": "assistant",
                    "content": "Transferring you to support for technical help.",
                }
            ],
            "active_agent": "support_agent",
        }
    return {
        "messages": msgs
        + [{"role": "assistant", "content": "[Sales] I can help with pricing and purchasing."}],
        "active_agent": "sales_agent",
    }


def support_agent_node(state: HandoffState):
    """Support agent - can hand off to sales."""
    msgs = state.get("messages", [])
    last = msgs[-1] if msgs else {}
    content = (last.get("content") or "").lower()
    if "buy" in content or "price" in content or "sales" in content:
        return {
            "messages": msgs
            + [
                {
                    "role": "assistant",
                    "content": "Transferring you to sales for purchasing help.",
                }
            ],
            "active_agent": "sales_agent",
        }
    return {
        "messages": msgs
        + [
            {
                "role": "assistant",
                "content": "[Support] I can help with technical issues and account problems.",
            }
        ],
        "active_agent": "support_agent",
    }


def route_after_agent(
    state: HandoffState,
) -> Literal["sales_agent", "support_agent", "__end__"]:
    """Route based on active_agent. End if no handoff (no 'Transferring' in last msg)."""
    msgs = state.get("messages", [])
    if msgs and "Transferring" in (msgs[-1].get("content") or ""):
        # Handoff - route to new agent
        return state.get("active_agent", "sales_agent") or "sales_agent"
    return "__end__"


def route_initial(state: HandoffState) -> Literal["sales_agent", "support_agent"]:
    """Initial route - default to sales."""
    return state.get("active_agent") or "sales_agent"


def _build_handoffs_graph():
    builder = StateGraph(HandoffState)
    builder.add_node("sales_agent", sales_agent_node)
    builder.add_node("support_agent", support_agent_node)

    builder.add_conditional_edges(START, route_initial, ["sales_agent", "support_agent"])
    builder.add_conditional_edges(
        "sales_agent", route_after_agent, ["sales_agent", "support_agent", END]
    )
    builder.add_conditional_edges(
        "support_agent", route_after_agent, ["sales_agent", "support_agent", END]
    )
    return builder.compile(checkpointer=InMemorySaver())


def demo_handoffs():
    """Sales ↔ Support handoffs based on user intent."""
    print("=== Multi-Agent Handoffs ===\n")

    graph = _build_handoffs_graph()

    # Scenario 1: User asks support question first
    print("Scenario: User has login trouble (starts with sales)")
    result = graph.invoke(
        {"messages": [{"role": "user", "content": "My account login is broken"}]},
        config={"configurable": {"thread_id": "handoff-1"}},
    )
    for m in result["messages"]:
        print(f"  {m['role']}: {m['content'][:70]}...")
    print(f"  active_agent: {result.get('active_agent')}")
    print()


if __name__ == "__main__":
    from utils.create_mermaid import build_and_save_mermaid

    output_dir = Path(__file__).resolve().parent.parent / "mermaids"
    output_dir.mkdir(parents=True, exist_ok=True)
    build_and_save_mermaid("07_handoffs", _build_handoffs_graph(), output_dir)

    demo_handoffs()
