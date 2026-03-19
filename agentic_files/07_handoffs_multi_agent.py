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

from langchain.messages import AIMessage, HumanMessage, ToolMessage, AnyMessage
from langchain.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from typing_extensions import NotRequired, TypedDict
from pathlib import Path

# --- Multiple agent subgraphs pattern ---
class HandoffState(TypedDict):
    messages: list[AnyMessage]
    active_agent: NotRequired[str]


@tool
def transfer_to_support(tool_call_id: str) -> Command:
    """Transfer control to support agent."""
    return Command(
        goto="support_agent",
        update={
            "active_agent": "support_agent",
            "messages": [
                ToolMessage(
                    content="Transferred to support agent",
                    tool_call_id=tool_call_id,
                )
            ],
        },
    )


@tool
def transfer_to_sales(tool_call_id: str) -> Command:
    """Transfer control to sales agent."""
    return Command(
        goto="sales_agent",
        update={
            "active_agent": "sales_agent",
            "messages": [
                ToolMessage(
                    content="Transferred to sales agent",
                    tool_call_id=tool_call_id,
                )
            ],
        },
    )


def sales_agent_node(state: HandoffState):
    """Sales agent can hand off to support via transfer tool."""
    msgs = state.get("messages", [])
    last = msgs[-1] if msgs else None
    content = getattr(last, "content", "").lower() if last else ""

    if "login" in content or "broken" in content or "support" in content:
        tool_call_id = "handoff_to_support"
        handoff_request = AIMessage(
            content="This sounds technical. I will transfer you to support.",
            tool_calls=[
                {
                    "id": tool_call_id,
                    "name": "transfer_to_support",
                    "args": {"tool_call_id": tool_call_id},
                }
            ],
        )
        handoff_cmd = transfer_to_support.invoke({"tool_call_id": tool_call_id})
        return Command(
            goto=handoff_cmd.goto,
            update={
                "active_agent": handoff_cmd.update["active_agent"],
                "messages": [handoff_request] + handoff_cmd.update["messages"],
            },
        )

    return {
        "messages": [AIMessage(content="[Sales] I can help with pricing and purchasing.")],
        "active_agent": "sales_agent",
    }


def support_agent_node(state: HandoffState):
    """Support agent can hand off to sales via transfer tool."""
    msgs = state.get("messages", [])
    last = msgs[-1] if msgs else None
    content = getattr(last, "content", "").lower() if last else ""

    if "buy" in content or "price" in content or "sales" in content:
        tool_call_id = "handoff_to_sales"
        handoff_request = AIMessage(
            content="This sounds like purchasing. I will transfer you to sales.",
            tool_calls=[
                {
                    "id": tool_call_id,
                    "name": "transfer_to_sales",
                    "args": {"tool_call_id": tool_call_id},
                }
            ],
        )
        handoff_cmd = transfer_to_sales.invoke({"tool_call_id": tool_call_id})
        return Command(
            goto=handoff_cmd.goto,
            update={
                "active_agent": handoff_cmd.update["active_agent"],
                "messages": [handoff_request] + handoff_cmd.update["messages"],
            },
        )

    return {
        "messages": [
            AIMessage(
                content="[Support] I can help with technical issues and account problems."
            )
        ],
        "active_agent": "support_agent",
    }


def route_after_agent(
    state: HandoffState,
) -> Literal["sales_agent", "support_agent", "__end__"]:
    """Route to next active agent only when a handoff tool message appears."""
    msgs = state.get("messages", [])
    if msgs and isinstance(msgs[-1], ToolMessage):
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
        {"messages": [HumanMessage(content="My account login is broken")]},
        config={"configurable": {"thread_id": "handoff-1"}},
    )
    for m in result["messages"]:
        role = getattr(m, "type", "message")
        content = getattr(m, "content", "")
        print(f"  {role}: {str(content)[:70]}...")
    print(f"  active_agent: {result.get('active_agent')}")


if __name__ == "__main__":
    from utils.create_mermaid import build_and_save_mermaid

    output_dir = Path(__file__).resolve().parent.parent / "mermaids"
    output_dir.mkdir(parents=True, exist_ok=True)
    build_and_save_mermaid("07_handoffs_multi_agent", _build_handoffs_graph(), output_dir)

    demo_handoffs()
