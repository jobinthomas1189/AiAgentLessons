"""
Simple LangGraph Interrupt Example - Approval Workflow
"""

from pathlib import Path
from typing import Literal, Optional, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt
from utils.create_mermaid import build_and_save_mermaid


class ApprovalState(TypedDict):
    action_details: str
    status: Optional[Literal["pending", "approved", "rejected"]]


def approval_node(state: ApprovalState):
    """Pause and wait for a human yes/no answer."""
    approved = interrupt(
        {
            "question": "Approve this action? (yes/no)",
            "details": state["action_details"],
        }
    )
    return {"status": "approved" if approved else "rejected"}


def route_after_approval(state: ApprovalState) -> str:
    """Use conditional edges to choose the next node."""
    return "proceed" if state["status"] == "approved" else "cancel"


def proceed_node(state: ApprovalState):
    return {"status": "approved"}


def cancel_node(state: ApprovalState):
    return {"status": "rejected"}


def _build_approval_graph():
    builder = StateGraph(ApprovalState)
    builder.add_node("approval", approval_node)
    builder.add_node("proceed", proceed_node)
    builder.add_node("cancel", cancel_node)
    builder.add_edge(START, "approval")
    builder.add_conditional_edges(
        "approval",
        route_after_approval,
        {"proceed": "proceed", "cancel": "cancel"},
    )
    builder.add_edge("proceed", END)
    builder.add_edge("cancel", END)
    return builder.compile(checkpointer=InMemorySaver())


def demo_approval_workflow():
    print("=== Approval Workflow ===")

    graph = _build_approval_graph()
    config = {"configurable": {"thread_id": "approval-123"}}

    result = graph.invoke(
        {"action_details": "Transfer $500", "status": "pending"},
        config,
    )
    payload = result["__interrupt__"][0].value

    print(f"\n{payload['question']}")
    print(f"Details: {payload['details']}")
    human_answer = input("Your response: ").strip().lower()
    approved = human_answer in {"y", "yes", "true", "1"}

    final = graph.invoke(Command(resume=approved), config)
    print("\nFinal status:", final["status"])


if __name__ == "__main__":

    output_dir = Path(__file__).resolve().parent.parent / "mermaids"
    output_dir.mkdir(parents=True, exist_ok=True)

    build_and_save_mermaid("03_interrupts_approval", _build_approval_graph(), output_dir)
    
    demo_approval_workflow()
