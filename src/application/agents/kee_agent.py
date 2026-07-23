from application.agents.kee.graph import KEEGraph
from application.dto.evolution_feed import EvolutionFeed
from application.dto.knowledge_package import KnowledgePackage
from application.dto.query_understanding_result import (
    QueryUnderstandingResult,
)
from application.dto.resource_reference import ResourceReference
from infrastructure.adapters.llm_adapter import LLMAdapter


class KEEAgent:
    """
    Knowledge Extraction Engine (KEE)

    Entry point for the autonomous KEE LangGraph.
    """

    def __init__(
        self,
        llm: LLMAdapter,
    ) -> None:
        self._graph = KEEGraph(
            llm=llm,
        ).build()

    def extract(
        self,
        goal: QueryUnderstandingResult,
        resources: list[ResourceReference],
    ) -> tuple[
        list[KnowledgePackage],
        list[EvolutionFeed],
    ]:
        state = {
            "goal": goal,
            "resources": resources,
            "memory": {},
            "knowledge_packages": [],
            "evolution_feeds": [],
            "current_resource": None,
            "current_observation": None,
            "finished": False,
        }

        state = self._graph.invoke(
            state,
        )

        if not state["evolution_feeds"]:
            state["evolution_feeds"] = self._derive_evolution_feeds(
                state["knowledge_packages"],
            )

        return (
            state["knowledge_packages"],
            state["evolution_feeds"],
        )
