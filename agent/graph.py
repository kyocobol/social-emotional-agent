from langgraph.graph import END, START, StateGraph

from agent.nodes import assistant, crisis_alerter
from agent.state import AgentState


def build_agent():
    builder = StateGraph(AgentState)
    builder.add_node("assistant", assistant)
    builder.add_node("crisis_alerter", crisis_alerter)

    builder.add_edge(START, "assistant")
    builder.add_edge("crisis_alerter", END)

    return builder.compile()
