from pydantic import BaseModel, Field


class KnowledgeEvolution(BaseModel):
    """
    Captures how this knowledge unit advanced its field.
    This is the core evolutionary information used by Ratlas.
    """

    previous_state: str | None = None

    problem: str | None = None

    catalyst: str | None = None

    innovation: str

    immediate_impact: str | None = None

    long_term_impact: str | None = None

    limitations: list[str] = Field(default_factory=list)

    open_problems: list[str] = Field(default_factory=list)

    significance: str | None = None
