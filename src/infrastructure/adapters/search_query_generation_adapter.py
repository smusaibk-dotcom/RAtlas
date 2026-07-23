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

        return self._llm.generate(request)
