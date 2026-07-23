from pydantic import BaseModel

from application.dto.knowledge_content import KnowledgeContent
from application.dto.knowledge_context import KnowledgeContext
from application.dto.knowledge_evidence import KnowledgeEvidence
from application.dto.knowledge_evolution import KnowledgeEvolution
from application.dto.knowledge_identity import KnowledgeIdentity
from application.dto.knowledge_metadata import KnowledgeMetadata
from application.dto.knowledge_relationship import (
    KnowledgeRelationship,
)
from application.dto.knowledge_timeline import KnowledgeTimeline


class KnowledgePackage(BaseModel):
    """
    Canonical representation of a single knowledge unit.
    """

    identity: KnowledgeIdentity

    content: KnowledgeContent

    timeline: KnowledgeTimeline

    evolution: KnowledgeEvolution

    relationships: KnowledgeRelationship

    evidence: KnowledgeEvidence

    context: KnowledgeContext

    metadata: KnowledgeMetadata
