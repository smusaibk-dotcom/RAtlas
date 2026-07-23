from abc import ABC, abstractmethod

from application.dto.search_query import SearchQuery
from application.dto.search_result import SearchResult


class SearchPort(ABC):
    @abstractmethod
    def search(
        self,
        query: SearchQuery,
    ) -> SearchResult:
        raise NotImplementedError
