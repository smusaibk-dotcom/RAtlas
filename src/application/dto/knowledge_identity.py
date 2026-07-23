from pydantic import BaseModel


class KnowledgeIdentity(BaseModel):
    """
    Identifies the extracted knowledge unit.
    """

    canonical_name: str

    aliases: list[str] = []

    category: str

    domain: str

    subdomain: str | None = None
