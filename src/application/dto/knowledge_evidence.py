from pydantic import BaseModel, Field

from application.dto.resource_reference import ResourceReference


class KnowledgeEvidence(BaseModel):
    """
    Evidence supporting this knowledge unit.
    Keeps every extracted fact traceable to its original source.
    """

    primary_sources: list[ResourceReference] = Field(default_factory=list)

    secondary_sources: list[ResourceReference] = Field(default_factory=list)

    confidence: float | None = None

    conflicting_sources: list[ResourceReference] = Field(default_factory=list)
