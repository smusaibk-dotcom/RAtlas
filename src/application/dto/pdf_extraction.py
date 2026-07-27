from typing import Any

from pydantic import BaseModel, Field


class PDFExtraction(BaseModel):
    """
    Complete rich extraction of a PDF.

    Nothing is normalized.
    Nothing is chunked.
    Everything remains in natural reading order.
    """

    pages: list[dict[str, Any]] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)
