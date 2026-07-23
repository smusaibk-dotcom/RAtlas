from application.dto.search_query_result import SearchQueryResult
from application.dto.search_result import SearchResult
from domain.ports.search_port import SearchPort


class SearchService:
    def __init__(
        self,
        search_port: SearchPort,
    ) -> None:
        self._search_port = search_port

    def search(
        self,
        search_queries: SearchQueryResult,
    ) -> list[SearchResult]:
        results: list[SearchResult] = []

        for query in search_queries.queries:
            result = self._search_port.search(query)
            results.append(result)

        return results
