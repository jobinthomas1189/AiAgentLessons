"""
Server graph registry for LangGraph dev.

This module exposes top-level graph objects that can be referenced from
langgraph.json as "<file>:<graph_variable>".
"""

from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path
from types import ModuleType
from typing import Any
from langgraph.graph import StateGraph, START, END

_THIS_DIR = Path(__file__).resolve().parent


def _load_module(file_name: str, module_name: str) -> ModuleType:
    target_path = _THIS_DIR / file_name
    spec = importlib.util.spec_from_file_location(module_name, target_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module from {target_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _graph_from_attr(file_name: str, attr_name: str, module_name: str) -> Any:
    module = _load_module(file_name, module_name)
    attr = getattr(module, attr_name)
    return attr() if inspect.isfunction(attr) else attr


def _graph_02_persistence() -> Any:
    module = _load_module("02_persistence.py", "agentic_files_lesson_02_persistence")
    builder = StateGraph(module.State)
    builder.add_node("node_a", module.node_a)
    builder.add_node("node_b", module.node_b)
    builder.add_edge(START, "node_a")
    builder.add_edge("node_a", "node_b")
    builder.add_edge("node_b", END)
    return builder.compile()


def _graph_03_interrupts() -> Any:
    module = _load_module("03_interrupts.py", "agentic_files_lesson_03_interrupts")
    builder = StateGraph(module.ApprovalState)
    builder.add_node("approval", module.approval_node)
    builder.add_node("proceed", module.proceed_node)
    builder.add_node("cancel", module.cancel_node)
    builder.add_edge(START, "approval")
    builder.add_edge("proceed", END)
    builder.add_edge("cancel", END)
    return builder.compile()


def _graph_04_durable_execution() -> Any:
    module = _load_module(
        "04_durable_execution.py",
        "agentic_files_lesson_04_durable_execution",
    )
    builder = StateGraph(module.StateWithTask)
    builder.add_node("call_api", module.call_api_with_task)
    builder.add_edge(START, "call_api")
    builder.add_edge("call_api", END)
    return builder.compile()


def _graph_05_multi_agent() -> Any:
    module = _load_module("05_multi_agent.py", "agentic_files_lesson_05_multi_agent")
    builder = StateGraph(module.MultiAgentState)
    builder.add_node("router", module.router_node)
    builder.add_node("coding_agent", module.coding_agent_node)
    builder.add_node("math_agent", module.math_agent_node)
    builder.add_node("general_agent", module.general_agent_node)
    builder.add_edge(START, "router")
    builder.add_conditional_edges(
        "router",
        module.route_after_router,
        ["coding_agent", "math_agent", "general_agent"],
    )
    builder.add_edge("coding_agent", END)
    builder.add_edge("math_agent", END)
    builder.add_edge("general_agent", END)
    return builder.compile()


def _graph_07_handoffs() -> Any:
    module = _load_module("07_handoffs.py", "agentic_files_lesson_07_handoffs")
    builder = StateGraph(module.HandoffState)
    builder.add_node("sales_agent", module.sales_agent_node)
    builder.add_node("support_agent", module.support_agent_node)
    builder.add_conditional_edges(
        START, module.route_initial, ["sales_agent", "support_agent"]
    )
    builder.add_conditional_edges(
        "sales_agent", module.route_after_agent, ["sales_agent", "support_agent", END]
    )
    builder.add_conditional_edges(
        "support_agent", module.route_after_agent, ["sales_agent", "support_agent", END]
    )
    return builder.compile()


# Graph factory exports (LangGraph server supports callable exports).
def graph_00_server_graph() -> Any:
    return _graph_from_attr(
        "00_server_graph.py",
        "graph",
        "agentic_files_lesson_00_server_graph",
    )

def graph_01_quickstart() -> Any:
    return _graph_from_attr(
        "01_quickstart.py",
        "build_graph_api_agent",
        "agentic_files_lesson_01_quickstart",
    )

def graph_02_persistence() -> Any:
    return _graph_02_persistence()

def graph_03_interrupts() -> Any:
    return _graph_03_interrupts()

def graph_04_durable_execution() -> Any:
    return _graph_04_durable_execution()

def graph_05_multi_agent() -> Any:
    return _graph_05_multi_agent()


def graph_06_subgraphs() -> Any:
    return _graph_from_attr(
        "06_subgraphs.py",
        "_build_call_subgraph_graph",
        "agentic_files_lesson_06_subgraphs",
    )

def graph_07_handoffs() -> Any:
    return _graph_07_handoffs()
