from pydantic import BaseModel, Field


class KnowledgeContent(BaseModel):
    """
    Human-readable explanation of the knowledge unit.
    Independent from its evolutionary role.
    """

    summary: str

    detailed_description: str | None = None

    keywords: list[str] = Field(default_factory=list)
