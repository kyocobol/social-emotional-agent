from langgraph.graph import END, START, StateGraph

from workflow.nodes import bdi_scorer, conversation_analyzer, siq_scorer
from workflow.state import WorkflowState


def build_workflow():
    builder = StateGraph(WorkflowState)

    builder.add_node("siq_scorer", siq_scorer)
    builder.add_node("bdi_scorer", bdi_scorer)
    builder.add_node("conversation_analyzer", conversation_analyzer)

    builder.add_edge(START, "siq_scorer")
    builder.add_edge(START, "bdi_scorer")
    builder.add_edge("siq_scorer", "conversation_analyzer")
    builder.add_edge("bdi_scorer", "conversation_analyzer")
    builder.add_edge("conversation_analyzer", END)

    return builder.compile()
