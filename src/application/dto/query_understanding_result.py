from enum import Enum

from pydantic import BaseModel


class QueryUnderstandingStatus(str, Enum):
    PROCEED = "PROCEED"
    NEED_CLARIFICATION = "NEED_CLARIFICATION"


class QueryUnderstandingResult(BaseModel):
    original_query: str
    refined_query: str
    intent: str
    research_domain: str
    confidence_score: float
    status: QueryUnderstandingStatus
    clarification_message: str | None = None
    clarification_options: list[str] = []
    ambiguity_reason: str | None = None
