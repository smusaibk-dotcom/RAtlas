from application.dto.coordinator_result import CoordinatorResult
from application.services.query_understanding_service import (
    QueryUnderstandingService,
)
from application.services.search_query_generation_service import (
    SearchQueryGenerationService,
)
from application.services.search_service import SearchService


class CoordinatorAgent:
    """
    Orchestrates Ratlas workflows.
    Responsibilities:
    - Coordinate research workflows (SF-1)
    - Coordinate knowledge source ingestion workflows (SF-2)
    This class delegates work to the appropriate services and adapters.
    It does not implement business logic itself.
    """

    def __init__(
        self,
        query_understanding_service: QueryUnderstandingService,
        search_query_generation_service: SearchQueryGenerationService,
        search_service: SearchService,
    ) -> None:
        self._query_understanding_service = query_understanding_service
        self._search_query_generation_service = search_query_generation_service
        self._search_service = search_service

    def start_research(
        self,
        query: str,
    ) -> CoordinatorResult:
        # Step 1: Understand the user's query
        understanding = self._query_understanding_service.analyze(query)

        # Step 2: Ask for clarification if needed
        if understanding.status == "NEED_CLARIFICATION":
            return CoordinatorResult(
                query_understanding=understanding,
                next_step="CLARIFICATION",
                message="The query requires clarification.",
            )

        # Step 3: Generate optimized search queries
        search_queries = self._search_query_generation_service.generate(understanding)

        # Step 4: Execute searches
        search_results = self._search_service.search(search_queries)

        # Step 5: Hand off to the next stage
        return CoordinatorResult(
            query_understanding=understanding,
            search_queries=search_queries,
            search_results=search_results,
            next_step="KNOWLEDGE_EXTRACTION",
        )
