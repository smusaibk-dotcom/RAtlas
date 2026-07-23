from pydantic import BaseModel


class KnowledgeMetadata(BaseModel):
    """
    Metadata describing how this knowledge unit was produced.
    This is not part of the knowledge itself.
    """

    extraction_confidence: float | None = None

    extraction_timestamp: str | None = None

    llm_provider: str | None = None

    llm_model: str | None = None

    verification_status: str | None = None
