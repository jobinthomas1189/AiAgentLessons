"""
LangGraph Quickstart - Calculator Agent
Source: https://docs.langchain.com/oss/python/langgraph/quickstart

Demonstrates two approaches:
1. Graph API: Define agent as a graph of nodes and edges
2. Functional API: Define agent as a single function with control flow

Requires: ANTHROPIC_API_KEY (or use OPENAI_API_KEY with init_chat_model)
"""

from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, HumanMessage, ToolMessage, AnyMessage
from typing_extensions import TypedDict, Annotated
from typing import Literal
import operator

# --- Graph API ---
from langgraph.graph import StateGraph, START, END

# 1. Define tools and model
model = init_chat_model("claude-sonnet-4-6", temperature=0)


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
model_with_tools = model.bind_tools(tools)


# 2. Define state
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int


# 3. Define model node
def llm_call(state: dict):
    """LLM decides whether to call a tool or not"""
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
        ],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }


# 4. Define tool node
def tool_node(state: dict):
    """Performs the tool call"""
    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(
            ToolMessage(content=str(observation), tool_call_id=tool_call["id"])
        )
    return {"messages": result}


# 5. Define end logic
def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    """Decide if we should continue or stop based on tool calls"""
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tool_node"
    return END


# 6. Build and compile the agent (Graph API)
def build_graph_api_agent():
    agent_builder = StateGraph(MessagesState)
    agent_builder.add_node("llm_call", llm_call)
    agent_builder.add_node("tool_node", tool_node)
    agent_builder.add_edge(START, "llm_call")
    agent_builder.add_conditional_edges(
        "llm_call", should_continue, ["tool_node", END]
    )
    agent_builder.add_edge("tool_node", "llm_call")
    return agent_builder.compile()


def run_graph_api_example():
    """Run the Graph API calculator agent."""
    print("=== Graph API - Calculator Agent ===\n")
    agent = build_graph_api_agent()
    result = agent.invoke({"messages": [HumanMessage(content="Add 3 and 4.")]})
    print("Messages:")
    for m in result["messages"]:
        m.pretty_print()
    print(f"\nLLM calls: {result.get('llm_calls', 0)}")


# --- Functional API ---
from langgraph.graph import add_messages
from langgraph.func import entrypoint, task
from langchain_core.messages import BaseMessage


@task
def call_llm(messages: list[BaseMessage]):
    """LLM decides whether to call a tool or not"""
    return model_with_tools.invoke(
        [
            SystemMessage(
                content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
            )
        ]
        + messages
    )


@task
def call_tool(tool_call):
    """Performs the tool call"""
    tool = tools_by_name[tool_call["name"]]
    return tool.invoke(tool_call["args"])


@entrypoint()
def functional_agent(messages: list[BaseMessage]):
    """Agent built with Functional API - uses control flow instead of graph."""
    model_response = call_llm(messages).result()
    while True:
        if not model_response.tool_calls:
            break
        tool_result_futures = [
            call_tool(tc) for tc in model_response.tool_calls
        ]
        raw_results = [fut.result() for fut in tool_result_futures]
        tool_messages = [
            ToolMessage(content=str(r), tool_call_id=tc["id"])
            for r, tc in zip(raw_results, model_response.tool_calls)
        ]
        messages = add_messages(messages, [model_response, *tool_messages])
        model_response = call_llm(messages).result()
    messages = add_messages(messages, model_response)
    return messages


def run_functional_api_example():
    """Run the Functional API calculator agent."""
    print("\n=== Functional API - Calculator Agent ===\n")
    messages = [HumanMessage(content="Add 3 and 4.")]
    for chunk in functional_agent.stream(messages, stream_mode="updates"):
        print(chunk)
        print()


if __name__ == "__main__":
    run_graph_api_example()
    run_functional_api_example()
