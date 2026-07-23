from typing import Any

from pydantic import BaseModel, Field


class CanonicalDocument(BaseModel):
    """
    A normalized representation of any knowledge source.

    Every extraction tool must produce this format.
    """

    resource_id: str | None = None

    source_url: str

    source_type: str

    title: str

    content: dict[str, Any] = Field(
        default_factory=lambda: {
            "text": "",
            "tables": [],
            "figures": [],
            "equations": [],
            "images": [],
            "code_blocks": [],
            "references": [],
            "links": [],
        },
        description=("Normalized multimodal document content."),
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Document metadata such as authors, publication date, journal, DOI, language, etc."
        ),
    )
