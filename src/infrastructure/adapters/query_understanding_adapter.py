import random
from pathlib import Path

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
        query = query.strip()
        if query.startswith("Original Query:"):
            original_query = (
                query.split("User Clarification:")[0].replace("Original Query:", "").strip()
            )

        else:
            original_query = query.strip()

        if "User Clarification:" in query:
            clarification = (
                query.split("User Clarification:")[1]
                .strip()
                .lower()
                .replace(" ", "_")
                .replace("/", "_")
            )

            fixture_name = f"{original_query.lower().replace(' ', '_')}__{clarification}"

        else:
            fixture_name = original_query.lower().replace(" ", "_").replace("/", "_")

        fixture_path = Path("tests/fixtures/query_understanding") / f"{fixture_name}.json"

        if DEV_MODE and USE_FIXTURES:
            print("LOAD:", fixture_name)

            cached = FixtureManager.load(
                "query_understanding",
                fixture_name,
            )

            if cached is not None:
                print("Loaded Query Understanding fixture.")

                return QueryUnderstandingResult.model_validate(cached)

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

        result = self._llm.generate(request)

        if DEV_MODE and USE_FIXTURES:
            if fixture_path.exists():
                fixture_name = f"{fixture_name}_{random.randint(100, 999)}"

            print("SAVE:", fixture_name)

            FixtureManager.save(
                "query_understanding",
                fixture_name,
                result.model_dump(),
            )

        return result
