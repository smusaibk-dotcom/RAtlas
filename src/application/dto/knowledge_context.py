from pydantic import BaseModel, Field


class KnowledgeContext(BaseModel):
    """
    Context surrounding the knowledge unit.
    These are not the evolution itself, but the environment
    in which it emerged.
    """

    people: list[str] = Field(default_factory=list)

    organizations: list[str] = Field(default_factory=list)

    locations: list[str] = Field(default_factory=list)

    cultures: list[str] = Field(default_factory=list)

    disciplines: list[str] = Field(default_factory=list)
