from pydantic import BaseModel

from application.dto.resource_reference import ResourceReference
from application.dto.search_query import SearchQuery


class SearchResult(BaseModel):
    search_query: SearchQuery

    requested_results: int

    retrieved_results: int

    response_time: float

    resources: list[ResourceReference]
