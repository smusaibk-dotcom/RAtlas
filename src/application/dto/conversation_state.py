from uuid import UUID

from pydantic import BaseModel

from application.dto.query_understanding_result import QueryUnderstandingResult
from application.dto.search_query_result import SearchQueryResult


class ConversationState(BaseModel):
    conversation_id: UUID

    original_query: str | None = None

    user_clarification: str | None = None

    query_understanding: QueryUnderstandingResult | None = None

    search_queries: SearchQueryResult | None = None

    current_stage: str = "QUERY_UNDERSTANDING"
