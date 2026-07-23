from application.dto.resource_reference import ResourceReference
from application.dto.search_query import SearchQuery
from application.dto.search_result import SearchResult
from domain.ports.search_port import SearchPort
from infrastructure.clients.tavily_client import TavilyClient


class SearchAdapter(SearchPort):
    def __init__(self) -> None:
        self._client = TavilyClient()

    def search(
        self,
        query: SearchQuery,
    ) -> SearchResult:
        response = self._client.search(
            query=query.query,
            max_results=query.max_results,
        )

        resources = [
            ResourceReference(
                title=result["title"],
                url=result["url"],
                provider="tavily",
                relevance_score=result.get("score"),
            )
            for result in response["results"]
        ]

        return SearchResult(
            search_query=query,
            requested_results=query.max_results,
            retrieved_results=len(resources),
            response_time=response["response_time"],
            resources=resources,
        )
