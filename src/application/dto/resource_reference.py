from typing import Any

from pydantic import BaseModel, Field


class ResourceReference(BaseModel):
    id: str | None = None

    title: str

    url: str

    resource_type: str | None = None

    provider: str

    relevance_score: float | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)
