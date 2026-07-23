from abc import ABC, abstractmethod

from application.dto.query_understanding_result import QueryUnderstandingResult


class QueryUnderstandingPort(ABC):
    @abstractmethod
    def analyze(self, query: str) -> QueryUnderstandingResult:
        """
        Analyze a user query and return structured understanding.
        """
        raise NotImplementedError
