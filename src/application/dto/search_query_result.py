from pydantic import BaseModel

from application.dto.search_query import SearchQuery


class SearchQueryResult(BaseModel):
    queries: list[SearchQuery]
