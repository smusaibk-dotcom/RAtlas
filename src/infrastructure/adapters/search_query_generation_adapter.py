from application.dto.llm_message import LLMMessage, MessageRole
from application.dto.llm_request import LLMRequest
from application.dto.query_understanding_result import (
    QueryUnderstandingResult,
)
from application.dto.search_query_result import SearchQueryResult
from domain.ports.llm_port import LLMPort
from domain.ports.search_query_generation_port import (
    SearchQueryGenerationPort,
)
from infrastructure.parsers.pydantic_parser import PydanticParser
from infrastructure.prompts.search_query_generation_prompt import (
    SYSTEM_PROMPT,
)
from shared.config import DEV_MODE, USE_FIXTURES
from shared.fixture_manager import FixtureManager


class SearchQueryGenerationAdapter(
    SearchQueryGenerationPort,
):
    def __init__(
        self,
        llm: LLMPort,
    ) -> None:
        self._llm = llm

    def generate(
        self,
        query: QueryUnderstandingResult,
    ) -> SearchQueryResult:
        fixture_name = (
            query.refined_query.lower()
            .strip()
            .replace(" ", "_")
            .replace("/", "_")
            .replace("(", "")
            .replace(")", "")
            .replace(",", "")
        )

        if DEV_MODE and USE_FIXTURES:
            print("LOAD:", fixture_name)

            cached = FixtureManager.load(
                "search_query_generation",
                fixture_name,
            )

            if cached is not None:
                print("Loaded Search Query fixture.")

                return SearchQueryResult.model_validate(cached)

        parser = PydanticParser.get_parser(SearchQueryResult)

        system_prompt = SYSTEM_PROMPT + "\n\n" + parser.get_format_instructions()

        request = LLMRequest(
            task="search_query_generation",
            messages=[
                LLMMessage(
                    role=MessageRole.SYSTEM,
                    content=system_prompt,
                ),
                LLMMessage(
                    role=MessageRole.USER,
                    content=query.model_dump_json(indent=2),
                ),
            ],
            response_model=SearchQueryResult,
            temperature=0.2,
        )

        result = self._llm.generate(request)

        if DEV_MODE and USE_FIXTURES:
            print("SAVE:", fixture_name)

            FixtureManager.save(
                "search_query_generation",
                fixture_name,
                result.model_dump(),
            )

        return result
