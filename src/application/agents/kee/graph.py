from langgraph.graph import END
from langgraph.graph import START
from langgraph.graph import StateGraph

from application.agents.kee.nodes import KEENodes
from application.agents.kee.states import KEEState
from infrastructure.adapters.llm_adapter import LLMAdapter


class KEEGraph:
    def __init__(
        self,
        llm: LLMAdapter,
    ) -> None:
        self._nodes = KEENodes(
            llm=llm,
        )

    def build(
        self,
    ):
        graph = StateGraph(
            KEEState,
        )

        graph.add_node(
            "reason",
            self._nodes.reason,
        )

        graph.add_node(
            "tool",
            self._nodes.tool,
        )

        graph.add_node(
            "chunk",
            self._nodes.chunk,
        )

        graph.add_node(
            "knowledge_package",
            self._nodes.knowledge_package,
        )

        graph.add_node(
            "evolution_feed",
            self._nodes.evolution_feed,
        )

        graph.add_edge(
            START,
            "reason",
        )

        graph.add_conditional_edges(
            "reason",
            self._nodes.router,
        )

        graph.add_edge(
            "tool",
            "chunk",
        )

        graph.add_edge(
            "chunk",
            "reason",
        )

        graph.add_edge(
            "knowledge_package",
            "reason",
        )

        graph.add_edge(
            "evolution_feed",
            END,
        )

        return graph.compile()
