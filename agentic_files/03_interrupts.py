"""
LangGraph Interrupts - Human-in-the-Loop
Source: https://docs.langchain.com/oss/python/langgraph/interrupts

Concepts:
- interrupt(): Pause execution and wait for external input
- Command(resume=...): Resume with the human's response
- thread_id: Persistent pointer for checkpointing
- Approval workflows, review-and-edit, validation patterns
"""

from typing import Literal, Optional, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt


# --- Approval Workflow ---
class ApprovalState(TypedDict):
    action_details: str
    status: Optional[Literal["pending", "approved", "rejected"]]


def approval_node(state: ApprovalState) -> Command:
    """Pause for human approval, then route to proceed or cancel."""
    decision = interrupt(
        {
            "question": "Approve this action?",
            "details": state["action_details"],
        }
    )
    return Command(goto="proceed" if decision else "cancel")


def proceed_node(state: ApprovalState):
    return {"status": "approved"}


def cancel_node(state: ApprovalState):
    return {"status": "rejected"}


def get_human_resume(interrupt_payload) -> str | bool:
    """Prompt user for input based on interrupt type. Returns value for Command(resume=...)."""
    if isinstance(interrupt_payload, dict):
        print(f"\n  {interrupt_payload.get('question', 'Input required')}")
        if "details" in interrupt_payload:
            print(f"  Details: {interrupt_payload['details']}")
        if "content" in interrupt_payload:
            print(f"  Current content: {interrupt_payload['content']}")
        raw = input("  Your response: ").strip()
        # Approval workflow expects True/False
        if "approve" in str(interrupt_payload.get("question", "")).lower():
            return raw.lower() in ("yes", "y", "true", "1")
        return raw if raw else interrupt_payload.get("content", "")
    print(f"\n  {interrupt_payload}")
    return input("  Your response: ").strip()


def run_with_human_input(graph, initial_input: dict, config: dict):
    """
    Run graph in a loop: on interrupt, prompt for human input and resume.
    Continues until graph completes (no more interrupts).
    """
    result = graph.invoke(initial_input, config)
    while "__interrupt__" in result and result["__interrupt__"]:
        interrupts = result["__interrupt__"]
        if len(interrupts) == 1:
            payload = interrupts[0].value
            resume_val = get_human_resume(payload)
            result = graph.invoke(Command(resume=resume_val), config)
        else:
            resume_map = {}
            for i in interrupts:
                print(f"\n  Interrupt: {i.value}")
                resume_map[i.id] = input(f"  Response for {i.value}: ").strip()
            result = graph.invoke(Command(resume=resume_map), config)
    return result


def demo_approval_workflow():
    """Demonstrate approval/reject workflow with interrupt."""
    print("=== Approval Workflow ===\n")

    builder = StateGraph(ApprovalState)
    builder.add_node("approval", approval_node)
    builder.add_node("proceed", proceed_node)
    builder.add_node("cancel", cancel_node)
    builder.add_edge(START, "approval")
    builder.add_edge("proceed", END)
    builder.add_edge("cancel", END)

    checkpointer = InMemorySaver()
    graph = builder.compile(checkpointer=checkpointer)

    config = {"configurable": {"thread_id": "approval-123"}}
    initial_input = {"action_details": "Transfer $500", "status": "pending"}

    # Run with human input loop - prompts when interrupt fires
    result = run_with_human_input(graph, initial_input, config)
    print("\nFinal status:", result["status"])
    print()


# --- Review and Edit ---
class ReviewState(TypedDict):
    generated_text: str


def review_node(state: ReviewState):
    """Pause for human to review and edit content."""
    updated = interrupt(
        {
            "instruction": "Review and edit this content",
            "content": state["generated_text"],
        }
    )
    return {"generated_text": updated}


def demo_review_and_edit():
    """Demonstrate review-and-edit pattern with human input in the loop."""
    print("=== Review and Edit ===\n")

    builder = StateGraph(ReviewState)
    builder.add_node("review", review_node)
    builder.add_edge(START, "review")
    builder.add_edge("review", END)

    checkpointer = InMemorySaver()
    graph = builder.compile(checkpointer=checkpointer)

    config = {"configurable": {"thread_id": "review-42"}}
    final = run_with_human_input(graph, {"generated_text": "Initial draft"}, config)
    print("\nFinal text:", final["generated_text"])
    print()


# --- Multiple Interrupts (parallel branches) ---
from typing import Annotated
import operator


class MultiInterruptState(TypedDict):
    vals: Annotated[list[str], operator.add]


def node_a(state):
    answer = interrupt("question_a")
    return {"vals": [f"a:{answer}"]}


def node_b(state):
    answer = interrupt("question_b")
    return {"vals": [f"b:{answer}"]}


def demo_multiple_interrupts():
    """Resume multiple interrupts with human input for each (map by ID)."""
    print("=== Multiple Interrupts ===\n")

    graph = (
        StateGraph(MultiInterruptState)
        .add_node("a", node_a)
        .add_node("b", node_b)
        .add_edge(START, "a")
        .add_edge(START, "b")
        .add_edge("a", END)
        .add_edge("b", END)
        .compile(checkpointer=InMemorySaver())
    )

    config = {"configurable": {"thread_id": "multi-1"}}
    result = run_with_human_input(graph, {"vals": []}, config)
    print("\nFinal state:", result)


if __name__ == "__main__":
    demo_approval_workflow()
    demo_review_and_edit()
    demo_multiple_interrupts()
