from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage

from workflow.prompts import (
    BDI_SCORER_PROMPT,
    CONVERSATION_ANALYZER_PROMPT,
    SIQ_SCORER_PROMPT,
)
from workflow.schemas import BDIScore, SIQScore
from workflow.state import WorkflowState


def siq_scorer(state: WorkflowState):
    """Scores SIQ-JR items based on the conversation history."""
    messages = state["messages"]
    conversation_history = "\n".join(
        f"- {'User' if isinstance(msg, HumanMessage) else 'Assistant'}: {msg.content}"
        for msg in messages
    )
    llm = init_chat_model(model="gpt-4o-mini").with_structured_output(SIQScore)
    siq_score = llm.invoke(
        [
            SystemMessage(content=SIQ_SCORER_PROMPT),
            HumanMessage(content=f"Conversation History:\n{conversation_history}"),
        ]
    )
    return {"siq_score": siq_score}


def bdi_scorer(state: WorkflowState):
    """Scores BDI-II items based on the conversation history."""
    messages = state["messages"]
    conversation_history = "\n".join(
        f"- {'User' if isinstance(msg, HumanMessage) else 'Assistant'}: {msg.content}"
        for msg in messages
    )
    llm = init_chat_model(model="gpt-4o-mini").with_structured_output(BDIScore)
    bdi_score = llm.invoke(
        [
            SystemMessage(content=BDI_SCORER_PROMPT),
            HumanMessage(content=f"Conversation History:\n{conversation_history}"),
        ]
    )
    return {"bdi_score": bdi_score}


def conversation_analyzer(state: WorkflowState):
    """Generates an analysis report from the conversation history and assessment scores."""
    messages = state["messages"]
    siq_score = state["siq_score"]
    bdi_score = state["bdi_score"]
    conversation_history = "\n".join(
        f"- {'User' if isinstance(msg, HumanMessage) else 'Assistant'}: {msg.content}"
        for msg in messages
    )
    llm = init_chat_model(model="gpt-4.1-mini")
    analysis_report = llm.invoke(
        [
            SystemMessage(content=CONVERSATION_ANALYZER_PROMPT),
            HumanMessage(
                content=(
                    f"Conversation History:\n{conversation_history}\n\n"
                    f"SIQ-JR Assessment Score:\n{siq_score.model_dump_json()}\n\n"
                    f"BDI-II Assessment Score:\n{bdi_score.model_dump_json()}"
                )
            ),
        ]
    ).content
    return {"analysis_report": analysis_report}
