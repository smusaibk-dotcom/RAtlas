from pydantic import BaseModel

from application.dto.query_understanding_result import (
    QueryUnderstandingResult,
)
from application.dto.search_query_result import (
    SearchQueryResult,
)
from application.dto.search_result import SearchResult


class CoordinatorResult(BaseModel):
    """
    Output of the Coordinator after orchestrating one stage of the workflow.
    """

    query_understanding: QueryUnderstandingResult

    search_queries: SearchQueryResult | None = None

    search_results: list[SearchResult] | None = None

    next_step: str

    message: str | None = None
