from application.dto.llm_message import LLMMessage, MessageRole
from application.dto.llm_request import LLMRequest
from application.dto.query_understanding_result import QueryUnderstandingResult
from domain.ports.llm_port import LLMPort
from domain.ports.query_understanding_port import QueryUnderstandingPort
from infrastructure.parsers.pydantic_parser import PydanticParser
from infrastructure.prompts.query_understanding_prompt import SYSTEM_PROMPT
from shared.config import DEV_MODE, USE_FIXTURES
from shared.fixture_manager import FixtureManager


class QueryUnderstandingAdapter(QueryUnderstandingPort):
    """
    Uses an LLM to analyze a user query.
    """

    def __init__(self, llm: LLMPort) -> None:
        self._llm = llm

    def analyze(self, query: str) -> QueryUnderstandingResult:
        parser = PydanticParser.get_parser(QueryUnderstandingResult)

        system_prompt = SYSTEM_PROMPT + "\n\n" + parser.get_format_instructions()

        request = LLMRequest(
            task="query_understanding",
            messages=[
                LLMMessage(
                    role=MessageRole.SYSTEM,
                    content=system_prompt,
                ),
                LLMMessage(
                    role=MessageRole.USER,
                    content=query,
                ),
            ],
            response_model=QueryUnderstandingResult,
            temperature=0.0,
        )

        return self._llm.generate(request)
