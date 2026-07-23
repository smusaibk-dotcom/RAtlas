from application.dto.query_understanding_result import QueryUnderstandingResult
from domain.ports.query_understanding_port import QueryUnderstandingPort


class QueryUnderstandingService:
    """
    Coordinates the query understanding process.
    """

    def __init__(self, query_understanding_port: QueryUnderstandingPort) -> None:
        self._query_understanding_port = query_understanding_port

    def analyze(self, query: str) -> QueryUnderstandingResult:
        return self._query_understanding_port.analyze(query)
