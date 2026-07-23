from typing import Any

from pydantic import BaseModel, Field


class Chunk(BaseModel):
    """
    One self-contained segment of a rich extraction.

    Every chunk preserves the original reading order,
    stays within the target token budget and contains
    all related artifacts required to understand it.
    """

    chunk_id: str

    source_type: str

    source_id: str

    content: Any = Field(
        description=(
            "Original chunk content exactly as produced "
            "by the chunker. It may contain text, images, "
            "tables, equations, code, captions or any "
            "combination depending on the source."
        )
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )
