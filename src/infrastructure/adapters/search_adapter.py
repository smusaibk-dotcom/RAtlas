from application.dto.resource_reference import ResourceReference
from application.dto.search_query import SearchQuery
from application.dto.search_result import SearchResult
from domain.ports.search_port import SearchPort
from infrastructure.clients.tavily_client import TavilyClient
from shared.config import DEV_MODE, USE_FIXTURES
from shared.fixture_manager import FixtureManager


class SearchAdapter(SearchPort):
    def __init__(self) -> None:
        self._client = TavilyClient()

    def search(
        self,
        query: SearchQuery,
    ) -> SearchResult:
        fixture_name = (
            query.query.lower()
            .strip()
            .replace(" ", "_")
            .replace("/", "_")
            .replace("(", "")
            .replace(")", "")
            .replace(",", "")
            .replace(":", "")
        )

        if DEV_MODE and USE_FIXTURES:
            print("LOAD SEARCH:", fixture_name)

            cached = FixtureManager.load(
                "search",
                fixture_name,
            )

            if cached is not None:
                print("Loaded Search fixture.")

                return SearchResult.model_validate(cached)

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

        result = SearchResult(
            search_query=query,
            requested_results=query.max_results,
            retrieved_results=len(resources),
            response_time=response["response_time"],
            resources=resources,
        )

        if DEV_MODE and USE_FIXTURES:
            print("SAVE SEARCH:", fixture_name)

            FixtureManager.save(
                "search",
                fixture_name,
                result.model_dump(),
            )

        return result
