import os
from tavily import TavilyClient as TavilySDK
from infrastructure.exceptions.search_exception import SearchException


class TavilyClient:
    def __init__(self) -> None:
        self._client = TavilySDK(api_key=os.getenv("TAVILY_API_KEY"))

    def search(
        self,
        query: str,
        max_results: int,
    ):
        try:
            return self._client.search(
                query=query,
                max_results=max_results,
            )

        except Exception as e:
            raise SearchException(str(e)) from e
