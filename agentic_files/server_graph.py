"""
Server-ready graph for LangGraph dev server.
Calculator agent - same as 01_quickstart, compiled for LangGraph API runtime.
Exported as `graph` for langgraph.json.
"""

from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, ToolMessage, AnyMessage
from typing_extensions import TypedDict, Annotated
from typing import Literal
import operator
from pathlib import Path
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END

# Load local env file for direct imports/runs (langgraph dev also loads via config).
load_dotenv(Path(__file__).with_name(".env"))


@tool
def multiply(a: int, b: int) -> int:
    """Multiply `a` and `b`."""
    return a * b


@tool
def add(a: int, b: int) -> int:
    """Adds `a` and `b`."""
    return a + b


@tool
def divide(a: int, b: int) -> float:
    """Divide `a` and `b`."""
    return a / b


tools = [add, multiply, divide]
tools_by_name = {t.name: t for t in tools}

model = init_chat_model("claude-sonnet-4-6", temperature=0)
model_with_tools = model.bind_tools(tools)


class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]


def llm_call(state: dict):
    return {
        "messages": [
            model_with_tools.invoke(
                [
                    SystemMessage(
                        content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
                    )
                ]
                + state["messages"]
            )
        ]
    }


def tool_node(state: dict):
    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(
            ToolMessage(content=str(observation), tool_call_id=tool_call["id"])
        )
    return {"messages": result}


def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tool_node"
    return END


builder = StateGraph(MessagesState)
builder.add_node("llm_call", llm_call)
builder.add_node("tool_node", tool_node)
builder.add_edge(START, "llm_call")
builder.add_conditional_edges("llm_call", should_continue, ["tool_node", END])
builder.add_edge("tool_node", "llm_call")

graph = builder.compile()
