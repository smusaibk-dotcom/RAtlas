from application.dto.query_understanding_result import QueryUnderstandingResult
from application.dto.search_query_result import SearchQueryResult
from domain.ports.search_query_generation_port import (
    SearchQueryGenerationPort,
)


class SearchQueryGenerationService:
    def __init__(
        self,
        port: SearchQueryGenerationPort,
    ):
        self._port = port

    def generate(
        self,
        query: QueryUnderstandingResult,
    ) -> SearchQueryResult:
        return self._port.generate(query)
