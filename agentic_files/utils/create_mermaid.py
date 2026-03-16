"""
Create Mermaid diagram images for each LangGraph lesson file.
Generates and stores .png images in the utils directory.
Run: python create_mermaid.py (from agentic_files or utils directory)

Note: PNG generation uses Mermaid.INK API and requires network access.
"""

import sys
from pathlib import Path

# Add parent to path for imports
SCRIPT_DIR = Path(__file__).resolve().parent
AGENTIC_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(AGENTIC_DIR))

OUTPUT_DIR = SCRIPT_DIR  # Store .png files in utils/


def get_mermaid_for_graph(graph) -> str:
    """Extract mermaid string from a compiled LangGraph."""
    try:
        g = graph.get_graph()
        return g.draw_mermaid()
    except Exception as e:
        return f"%% Error generating mermaid: {e}\nflowchart TB\n  error[{str(e)}]"


def save_mermaid_png(graph, output_path: Path) -> bool:
    """Save graph as PNG image. Returns True on success. Requires network (Mermaid.INK API)."""
    try:
        g = graph.get_graph()
        png_bytes = g.draw_mermaid_png(max_retries=3, retry_delay=2)
        output_path.write_bytes(png_bytes)
        return True
    except Exception as e:
        print(f"    PNG error: {e}")
        return False


def build_and_save_mermaid(
    name: str, graph, output_dir: Path, print_mermaid: bool = False, save_png: bool = True
) -> tuple[str, bool]:
    """Save graph as .png image, return (mermaid_str, success)."""
    mermaid = get_mermaid_for_graph(graph)
    png_path = output_dir / f"{name}.png"
    png_ok = save_mermaid_png(graph, png_path) if save_png else False
    if print_mermaid:
        print(f"\n--- {name} ---\n{mermaid}\n")
    return mermaid, png_ok


def main():
    from typing import Annotated, Literal, Optional, NotRequired
    from typing_extensions import TypedDict
    from operator import add

    from langgraph.checkpoint.memory import InMemorySaver
    from langgraph.graph import StateGraph, START, END

    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    all_results = []

    # --- 01 Quickstart: Graph API (calculator agent) ---
    def _quickstart_state():
        from typing_extensions import TypedDict, Annotated
        import operator
        from langchain.messages import AnyMessage
        class S(TypedDict):
            messages: Annotated[list, operator.add]
            llm_calls: int
        return S
    try:
        S = _quickstart_state()
        def llm_stub(s): return s
        def tool_stub(s): return s
        def route(s): return "tool_node" if s.get("_tool_call") else "__end__"
        w = StateGraph(S)
        w.add_node("llm_call", llm_stub)
        w.add_node("tool_node", tool_stub)
        w.add_edge(START, "llm_call")
        w.add_conditional_edges("llm_call", lambda s: "tool_node" if True else "__end__", ["tool_node", "__end__"])
        w.add_edge("tool_node", "llm_call")
        g = w.compile()
        m, ok = build_and_save_mermaid("01_quickstart", g, output_dir)
        all_results.append(("01_quickstart", ok))
        print(f"01_quickstart: {'OK' if ok else 'FAIL'}")
    except Exception as e:
        all_results.append(("01_quickstart", False))
        print(f"01_quickstart: SKIP - {e}")

    # --- 02 Persistence ---
    try:
        class State(TypedDict):
            foo: str
            bar: Annotated[list[str], add]
        def na(s): return {"foo": "a", "bar": ["a"]}
        def nb(s): return {"foo": "b", "bar": ["b"]}
        w = StateGraph(State)
        w.add_node("node_a", na)
        w.add_node("node_b", nb)
        w.add_edge(START, "node_a")
        w.add_edge("node_a", "node_b")
        w.add_edge("node_b", END)
        g = w.compile(checkpointer=InMemorySaver())
        m, ok = build_and_save_mermaid("02_persistence", g, output_dir)
        all_results.append(("02_persistence", ok))
        print(f"02_persistence: {'OK' if ok else 'FAIL'}")
    except Exception as e:
        all_results.append(("02_persistence", False))
        print(f"02_persistence: SKIP - {e}")

    # --- 03 Interrupts (3 graphs) - nodes labeled to show interrupt points ---
    try:
        class ApprovalState(TypedDict):
            action_details: str
            status: Optional[str]
        def approval_stub(s): return s
        def proceed_stub(s): return {"status": "approved"}
        def cancel_stub(s): return {"status": "rejected"}
        w = StateGraph(ApprovalState)
        w.add_node("approval_interrupt", approval_stub)  # interrupt() called here
        w.add_node("proceed", proceed_stub)
        w.add_node("cancel", cancel_stub)
        w.add_edge(START, "approval_interrupt")
        w.add_conditional_edges("approval_interrupt", lambda s: "proceed", ["proceed", "cancel"])
        w.add_edge("proceed", END)
        w.add_edge("cancel", END)
        g = w.compile(checkpointer=InMemorySaver())
        m, ok = build_and_save_mermaid("03_interrupts_approval", g, output_dir)
        all_results.append(("03_interrupts_approval", ok))
        print(f"03_interrupts_approval: {'OK' if ok else 'FAIL'}")
    except Exception as e:
        all_results.append(("03_interrupts_approval", False))
        print(f"03_interrupts_approval: SKIP - {e}")

    try:
        class ReviewState(TypedDict):
            generated_text: str
        def review_stub(s): return s
        w = StateGraph(ReviewState)
        w.add_node("review_interrupt", review_stub)  # interrupt() called here
        w.add_edge(START, "review_interrupt")
        w.add_edge("review_interrupt", END)
        g = w.compile(checkpointer=InMemorySaver())
        m, ok = build_and_save_mermaid("03_interrupts_review", g, output_dir)
        all_results.append(("03_interrupts_review", ok))
        print(f"03_interrupts_review: {'OK' if ok else 'FAIL'}")
    except Exception as e:
        all_results.append(("03_interrupts_review", False))
        print(f"03_interrupts_review: SKIP - {e}")

    try:
        class MultiState(TypedDict):
            vals: Annotated[list[str], add]
        def na(s): return {"vals": ["a"]}
        def nb(s): return {"vals": ["b"]}
        w = StateGraph(MultiState)
        w.add_node("a_interrupt", na)  # interrupt() called here
        w.add_node("b_interrupt", nb)  # interrupt() called here
        w.add_edge(START, "a_interrupt")
        w.add_edge(START, "b_interrupt")
        w.add_edge("a_interrupt", END)
        w.add_edge("b_interrupt", END)
        g = w.compile(checkpointer=InMemorySaver())
        m, ok = build_and_save_mermaid("03_interrupts_multi", g, output_dir)
        all_results.append(("03_interrupts_multi", ok))
        print(f"03_interrupts_multi: {'OK' if ok else 'FAIL'}")
    except Exception as e:
        all_results.append(("03_interrupts_multi", False))
        print(f"03_interrupts_multi: SKIP - {e}")

    # --- 04 Durable Execution ---
    try:
        class SimpleState(TypedDict):
            step: str
            count: int
        def na(s): return {"step": "a", "count": s.get("count", 0) + 1}
        def nb(s): return {"step": "b", "count": s.get("count", 0) + 1}
        w = StateGraph(SimpleState)
        w.add_node("node_a", na)
        w.add_node("node_b", nb)
        w.add_edge(START, "node_a")
        w.add_edge("node_a", "node_b")
        w.add_edge("node_b", END)
        g = w.compile(checkpointer=InMemorySaver())
        m, ok = build_and_save_mermaid("04_durable_execution", g, output_dir)
        all_results.append(("04_durable_execution", ok))
        print(f"04_durable_execution: {'OK' if ok else 'FAIL'}")
    except Exception as e:
        all_results.append(("04_durable_execution", False))
        print(f"04_durable_execution: SKIP - {e}")

    # --- 05 Multi-Agent (Router) ---
    try:
        class MultiAgentState(TypedDict):
            messages: list
            routed_to: str | None
        def router(s): return {"routed_to": "general_agent"}
        def coding(s): return s
        def math(s): return s
        def general(s): return s
        w = StateGraph(MultiAgentState)
        w.add_node("router", router)
        w.add_node("coding_agent", coding)
        w.add_node("math_agent", math)
        w.add_node("general_agent", general)
        w.add_edge(START, "router")
        w.add_conditional_edges("router", lambda s: s.get("routed_to") or "general_agent",
                               ["coding_agent", "math_agent", "general_agent"])
        w.add_edge("coding_agent", END)
        w.add_edge("math_agent", END)
        w.add_edge("general_agent", END)
        g = w.compile(checkpointer=InMemorySaver())
        m, ok = build_and_save_mermaid("05_multi_agent", g, output_dir)
        all_results.append(("05_multi_agent", ok))
        print(f"05_multi_agent: {'OK' if ok else 'FAIL'}")
    except Exception as e:
        all_results.append(("05_multi_agent", False))
        print(f"05_multi_agent: SKIP - {e}")

    # --- 06 Subgraphs ---
    try:
        class SubState(TypedDict):
            bar: str
            baz: str
        def sg1(s): return {"baz": "baz"}
        def sg2(s): return {"bar": s["bar"] + s["baz"]}
        sub = StateGraph(SubState)
        sub.add_node("subgraph_node_1", sg1)
        sub.add_node("subgraph_node_2", sg2)
        sub.add_edge(START, "subgraph_node_1")
        sub.add_edge("subgraph_node_1", "subgraph_node_2")
        sub.add_edge("subgraph_node_2", END)
        subgraph = sub.compile()

        class ParentState(TypedDict):
            foo: str
        def n1(s): return {"foo": "hi! " + s["foo"]}
        def call_sg(s): return {"foo": s["foo"] + "x"}
        w = StateGraph(ParentState)
        w.add_node("node_1", n1)
        w.add_node("node_2", subgraph)
        w.add_edge(START, "node_1")
        w.add_edge("node_1", "node_2")
        w.add_edge("node_2", END)
        g = w.compile()
        m, ok = build_and_save_mermaid("06_subgraphs", g, output_dir)
        all_results.append(("06_subgraphs", ok))
        print(f"06_subgraphs: {'OK' if ok else 'FAIL'}")
    except Exception as e:
        all_results.append(("06_subgraphs", False))
        print(f"06_subgraphs: SKIP - {e}")

    # --- 07 Handoffs ---
    try:
        class HandoffState(TypedDict):
            messages: list
            active_agent: NotRequired[str]
        def sales(s): return s
        def support(s): return s
        def route_init(s): return s.get("active_agent") or "sales_agent"
        def route_after(s): return "__end__"
        w = StateGraph(HandoffState)
        w.add_node("sales_agent", sales)
        w.add_node("support_agent", support)
        w.add_conditional_edges(START, route_init, ["sales_agent", "support_agent"])
        w.add_conditional_edges("sales_agent", route_after, ["sales_agent", "support_agent", "__end__"])
        w.add_conditional_edges("support_agent", route_after, ["sales_agent", "support_agent", "__end__"])
        g = w.compile(checkpointer=InMemorySaver())
        m, ok = build_and_save_mermaid("07_handoffs", g, output_dir)
        all_results.append(("07_handoffs", ok))
        print(f"07_handoffs: {'OK' if ok else 'FAIL'}")
    except Exception as e:
        all_results.append(("07_handoffs", False))
        print(f"07_handoffs: SKIP - {e}")

    # Summary
    print("\n--- Summary ---")
    success = sum(1 for _, ok in all_results if ok)
    total = len(all_results)
    print(f"Saved {success}/{total} graphs to {output_dir}")
    for name, ok in all_results:
        status = "OK" if ok else "FAIL"
        print(f"  {name}.png: {status}")


if __name__ == "__main__":
    main()
