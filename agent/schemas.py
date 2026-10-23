from typing import Literal

from pydantic import BaseModel, Field


class ChatResponse(BaseModel):
    message: str = Field(description="Response message to the user")
    suicidal_ideation_level: Literal["none", "low", "medium", "high"] = Field(
        description="Current level of suicidal ideation"
    )
    depression_level: Literal["none", "low", "medium", "high"] = Field(
        description="Current level of depression"
    )
    previous_suicide_attempt: bool = Field(
        description="Whether the user has mentioned a previous suicide attempt"
    )
    has_specific_suicide_plan: bool = Field(
        description="Whether the user has mentioned a specific plan for suicide"
    )
    recent_severe_stress_event: bool = Field(
        description="Whether the user has experienced a severe stress event recently"
    )
    family_or_friend_suicide_history: bool = Field(
        description="Whether a family member or close friend has died by suicide"
    )
    should_continue: bool = Field(
        description="Whether to continue the conversation or end it"
    )
