from abc import ABC, abstractmethod

from application.dto.query_understanding_result import QueryUnderstandingResult
from application.dto.search_query_result import SearchQueryResult


class SearchQueryGenerationPort(ABC):
    @abstractmethod
    def generate(
        self,
        query: QueryUnderstandingResult,
    ) -> SearchQueryResult:
        raise NotImplementedError
