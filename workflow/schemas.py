from typing import Literal

from pydantic import BaseModel, Field


class ScoredItem(BaseModel):
    item: str = Field(description="Item name (e.g., 'better_off_not_alive', 'sadness')")
    score: int = Field(description="Score assigned to this item")
    evidence: str = Field(description="User's quote or behavior supporting this score")


class SIQScore(BaseModel):
    better_off_not_alive: int = Field(
        ge=0, le=6, description="Thought it would be better if not alive"
    )
    killing_self: int = Field(ge=0, le=6, description="Thought about killing myself")
    how_to_kill_self: int = Field(
        ge=0, le=6, description="Thought about how I would kill myself"
    )
    when_to_kill_self: int = Field(
        ge=0, le=6, description="Thought about when I would kill myself"
    )
    people_dying: int = Field(ge=0, le=6, description="Thought about people dying")
    death: int = Field(ge=0, le=6, description="Thought about death")
    suicide_note: int = Field(
        ge=0, le=6, description="Thought about what to write in a suicide note"
    )
    writing_will: int = Field(ge=0, le=6, description="Thought about writing a will")
    telling_plan: int = Field(
        ge=0, le=6, description="Thought about telling people I plan to kill myself"
    )
    others_reaction: int = Field(
        ge=0, le=6, description="Thought about how people would feel if I killed myself"
    )
    wished_dead: int = Field(ge=0, le=6, description="Wished I were dead")
    death_as_solution: int = Field(
        ge=0, le=6, description="Thought that killing myself would solve my problems"
    )
    others_happier: int = Field(
        ge=0, le=6, description="Thought that others would be happier if I was dead"
    )
    never_born: int = Field(ge=0, le=6, description="Wished that I had never been born")
    no_one_cares: int = Field(
        ge=0, le=6, description="Thought that no one cared if I lived or died"
    )
    total_score: int = Field(ge=0, le=90, description="Sum of all 15 items")
    at_risk: bool = Field(
        description="Whether the user is at-risk for suicide based on total score"
    )
    scored_items: list[ScoredItem] = Field(
        description="Items scorable from conversation with supporting evidence"
    )


class BDIScore(BaseModel):
    sadness: int = Field(ge=0, le=3, description="Sadness level")
    pessimism: int = Field(ge=0, le=3, description="Discouragement about future")
    past_failure: int = Field(ge=0, le=3, description="Sense of failure")
    loss_of_pleasure: int = Field(ge=0, le=3, description="Loss of pleasure")
    guilty_feelings: int = Field(ge=0, le=3, description="Guilty feelings")
    punishment_feelings: int = Field(ge=0, le=3, description="Feeling punished")
    self_dislike: int = Field(ge=0, le=3, description="Self-dislike")
    self_criticalness: int = Field(ge=0, le=3, description="Self-criticalness")
    suicidal_thoughts: int = Field(
        ge=0, le=3, description="Suicidal thoughts or wishes"
    )
    crying: int = Field(ge=0, le=3, description="Crying changes")
    agitation: int = Field(ge=0, le=3, description="Restlessness or agitation")
    loss_of_interest: int = Field(
        ge=0, le=3, description="Loss of interest in other people or activities"
    )
    indecisiveness: int = Field(ge=0, le=3, description="Decision-making difficulty")
    worthlessness: int = Field(ge=0, le=3, description="Feelings of worthlessness")
    loss_of_energy: int = Field(ge=0, le=3, description="Loss of energy")
    sleep_changes: int = Field(ge=0, le=3, description="Changes in sleeping pattern")
    irritability: int = Field(ge=0, le=3, description="Irritability")
    appetite_changes: int = Field(ge=0, le=3, description="Changes in appetite")
    concentration_difficulty: int = Field(
        ge=0, le=3, description="Concentration difficulty"
    )
    tiredness: int = Field(ge=0, le=3, description="Tiredness or fatigue")
    loss_of_interest_in_sex: int = Field(
        ge=0, le=3, description="Loss of interest in sex"
    )
    total_score: int = Field(ge=0, le=63, description="Sum of all 21 items")
    depression_level: Literal["minimal", "mild", "moderate", "severe"] = Field(
        description="Level of depression based on total score"
    )
    scored_items: list[ScoredItem] = Field(
        description="Items scorable from conversation with supporting evidence"
    )
