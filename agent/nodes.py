from typing import Literal

from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.types import Command

from agent.prompts import ASSISTANT_PROMPT
from agent.schemas import ChatResponse
from agent.state import AgentState


def assistant(state: AgentState) -> Command[Literal["crisis_alerter", "__end__"]]:
    """Generates an empathetic response with suicide risk factor extraction."""
    messages = state["messages"]
    user_input = state["user_input"]
    llm = init_chat_model(model="gpt-4o-mini").with_structured_output(ChatResponse)
    response = llm.invoke(
        [
            SystemMessage(content=ASSISTANT_PROMPT),
            *messages,
            HumanMessage(content=user_input),
        ]
    )

    update = {
        "messages": [
            HumanMessage(content=user_input),
            AIMessage(content=response.message),
        ],
        "last_response": response,
    }

    if response.has_specific_suicide_plan or (
        response.suicidal_ideation_level in ["medium", "high"]
        and response.depression_level in ["medium", "high"]
        and response.previous_suicide_attempt
        and response.recent_severe_stress_event
        and response.family_or_friend_suicide_history
    ):
        return Command(update=update, goto="crisis_alerter")

    return Command(update=update, goto="__end__")


def crisis_alerter(state: AgentState):
    """Sends a suicide crisis alert based on the extracted risk factors."""
    return
