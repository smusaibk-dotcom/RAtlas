from pydantic import BaseModel

from application.dto.knowledge_evolution import KnowledgeEvolution
from application.dto.knowledge_identity import KnowledgeIdentity
from application.dto.knowledge_relationship import KnowledgeRelationship
from application.dto.knowledge_timeline import KnowledgeTimeline


class EvolutionFeed(BaseModel):
    """
    Distilled evolutionary information required by the
    Evolution Engine to construct the evolution graph.
    """

    identity: KnowledgeIdentity

    timeline: KnowledgeTimeline

    evolution: KnowledgeEvolution

    relationships: KnowledgeRelationship
