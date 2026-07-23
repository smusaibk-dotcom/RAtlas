from pydantic import BaseModel, Field


class SearchQuery(BaseModel):
    query: str

    reason: str | None = None

    priority: int = Field(
        ge=1,
        description="Lower number means higher priority.",
    )

    max_results: int = Field(
        gt=0,
    )
