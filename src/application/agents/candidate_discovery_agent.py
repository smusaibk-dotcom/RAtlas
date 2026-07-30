from application.dto.llm_request import LLMRequest
from infrastructure.adapters.llm_adapter import LLMAdapter
from infrastructure.prompts.candidate_discovery_system_prompt import SYSTEM_PROMPT
from infrastructure.prompts.candidate_discovery_user_prompt import (
    build_candidate_discovery_user_prompt,
)
from application.dto.chunk import Chunk
from application.dto.candidate_discovery_response import CandidateDiscoveryResponse
from application.dto.llm_message import LLMMessage, MessageRole


class CandidateDiscoveryAgent:
    def __init__(self):
        self._llm = LLMAdapter()

    def run(
        self,
        chunk: Chunk,
    ) -> CandidateDiscoveryResponse:
        user_prompt = build_candidate_discovery_user_prompt(
            chunk,
        )

        request = LLMRequest(
            task="candidate_discovery",
            messages=[
                LLMMessage(
                    role=MessageRole.SYSTEM,
                    content=SYSTEM_PROMPT,
                ),
                LLMMessage(
                    role=MessageRole.USER,
                    content=user_prompt,
                ),
            ],
            response_model=CandidateDiscoveryResponse,
        )

        response = self._llm.generate(
            request,
        )

        return response
