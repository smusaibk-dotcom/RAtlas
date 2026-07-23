from pydantic import BaseModel, Field


class KnowledgeRelationship(BaseModel):
    """
    Describes how this knowledge unit relates to other
    knowledge units in the evolution of a domain.
    """

    builds_upon: list[str] = Field(default_factory=list)

    inspired_by: list[str] = Field(default_factory=list)

    influenced: list[str] = Field(default_factory=list)

    replaces: list[str] = Field(default_factory=list)

    parallel_developments: list[str] = Field(default_factory=list)

    competing_approaches: list[str] = Field(default_factory=list)
