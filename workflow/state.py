from collections.abc import Sequence
from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

from workflow.schemas import BDIScore, SIQScore


class WorkflowState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    siq_score: SIQScore
    bdi_score: BDIScore
    analysis_report: str
