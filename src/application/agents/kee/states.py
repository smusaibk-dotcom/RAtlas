from typing import TypedDict

from application.dto.evolution_feed import EvolutionFeed
from application.dto.knowledge_package import KnowledgePackage
from application.dto.query_understanding_result import (
    QueryUnderstandingResult,
)
from application.dto.resource_reference import ResourceReference


class KEEState(TypedDict):
    """
    Shared state flowing through the
    Knowledge Extraction Engine.
    """

    # ===========================
    # Goal
    # ===========================

    goal: QueryUnderstandingResult

    # ===========================
    # Input Resources
    # ===========================

    resources: list[ResourceReference]

    # ===========================
    # Current Processing
    # ===========================

    current_resource: ResourceReference | None

    current_chunk: str | None

    current_observation: object | None

    # ===========================
    # Outputs
    # ===========================

    knowledge_packages: list[KnowledgePackage]

    evolution_feeds: list[EvolutionFeed]

    # ===========================
    # Working Memory
    # ===========================

    memory: dict

    # ===========================
    # Lifecycle
    # ===========================

    finished: bool
