from pydantic import BaseModel, Field

from application.dto.search_result import SearchResult


class SearchDebugResult(BaseModel):
    search_results: list[SearchResult]

    total_queries: int

    total_requested: int

    total_retrieved: int

    total_resources: int

    pdf_count: int

    html_count: int

    youtube_count: int

    other_count: int

    duplicate_count: int

    providers: dict[str, int] = Field(default_factory=dict)

    elapsed_time: float

    logs: list[str] = Field(default_factory=list)
