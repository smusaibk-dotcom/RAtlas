from application.agents.kee.states import KEEState
from application.dto.llm_request import LLMRequest
from infrastructure.adapters.llm_adapter import LLMAdapter
from infrastructure.tools.tools import (
    HTMLTool,
    PDFTool,
    ArxivTool,
    PubMedTool,
    GitHubTool,
    YouTubeTool,
    ImageTool,
)

from infrastructure.prompts.kee_system_prompt import (
    build_kee_system_prompt,
)
from infrastructure.prompts.kee_reason_user_prompt import (
    build_kee_user_prompt,
)

from application.dto.llm_message import (
    LLMMessage,
    MessageRole,
)

from application.services.chunker import Chunker


class KEENodes:
    def __init__(
        self,
        llm: LLMAdapter,
    ) -> None:
        self._llm = llm

        self._chunker = Chunker()

        self._tools = {
            "html": HTMLTool(),
            "pdf": PDFTool(),
            "arxiv": ArxivTool(),
            "pubmed": PubMedTool(),
            "github": GitHubTool(),
            "youtube": YouTubeTool(),
            "image": ImageTool(),
        }

    def reason(
        self,
        state: KEEState,
    ) -> KEEState:
        request = LLMRequest(
            task="knowledge_extraction",
            messages=[
                LLMMessage(
                    role=MessageRole.SYSTEM,
                    content=build_kee_system_prompt(),
                ),
                LLMMessage(
                    role=MessageRole.USER,
                    content=build_kee_reason_user_prompt(
                        state=state,
                        tools=list(self._tools.keys()),
                    ),
                ),
            ],
            response_model=dict,
        )

        observation = self._llm.generate(
            request=request,
        )

        state["current_observation"] = observation
        return state

    def tool(
        self,
        state: KEEState,
    ) -> KEEState:
        """
        Execute the tool selected by the agent.
        """

        observation = state["current_observation"]

        tool_name = observation["tool"]

        capability = observation["capability"]

        arguments = observation["arguments"]

        tool = self._tools[tool_name]

        result = getattr(
            tool,
            capability,
        )(
            **arguments,
        )

        state["memory"]["tool_output"] = result

        state["current_observation"] = {
            "action": "chunk",
        }

        return state

    def chunk(
        self,
        state: KEEState,
    ) -> KEEState:
        """
        Split the current CanonicalDocument
        into deterministic chunks.
        """

        tool.output = state["memory"]["tool_output"]

        chunks = self._chunker.chunk(
            tool_output,
        )

        state["memory"]["chunks"] = chunks

        state["current_observation"] = {
            "action": "knowledge_package",
        }

        return state

    def knowledge_package(
        self,
        state: KEEState,
    ) -> KEEState:
        """
        Generate or update Knowledge Packages.
        """

        request = LLMRequest(
            task="knowledge_package_generation",
            messages=[
                LLMMessage(
                    role=MessageRole.SYSTEM,
                    content=build_kee_system_prompt(),
                ),
                LLMMessage(
                    role=MessageRole.USER,
                    content=build_kee_reason_user_prompt(
                        state=state,
                        tools=list(self._tools.keys()),
                    ),
                ),
            ],
            response_model=dict,
        )

        return state

    def evolution_feed(
        self,
        state: KEEState,
    ) -> KEEState:
        """
        Derive Evolution Feeds from
        Knowledge Packages.
        """

        state["evolution_feeds"] = self._derive_evolution_feeds(
            state["knowledge_packages"],
        )

        return state

    def _derive_evolution_feeds(
        self,
        packages: list[KnowledgePackage],
    ) -> list[EvolutionFeed]:
        """
        Temporary implementation.

        This method will later be replaced by a dedicated
        LangGraph node responsible for deriving
        Evolution Feeds from the generated
        Knowledge Packages.
        """

        raise NotImplementedError
