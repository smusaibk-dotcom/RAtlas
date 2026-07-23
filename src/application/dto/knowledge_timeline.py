from pydantic import BaseModel


class KnowledgeTimeline(BaseModel):
    """
    Represents when a knowledge unit existed or emerged.
    Works across all domains.
    """

    start_year: int | None = None

    end_year: int | None = None

    era: str | None = None

    chronological_confidence: float | None = None
