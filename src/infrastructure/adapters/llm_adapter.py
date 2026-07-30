import os
from typing import Any

from dotenv import load_dotenv

from application.dto.llm_request import LLMRequest
from domain.ports.llm_port import LLMPort
from infrastructure.clients.huggingface_client import HuggingFaceClient

load_dotenv()


class LLMAdapter(LLMPort):
    """
    Central gateway for all LLM interactions.

    Responsibilities:
    - Select the appropriate model for the requested task.
    - Delegate the request to the configured LLM provider.
    """

    def __init__(self) -> None:
        self._hf_client = HuggingFaceClient()

        self._task_to_model = {
            "query_understanding": os.getenv("QUERY_UNDERSTANDING_MODEL"),
            "search_query_generation": os.getenv("SEARCH_QUERY_GENERATION_MODEL"),
            "candidate_discovery": os.getenv("CANDIDATE_DISCOVERY_MODEL"),
            "graph_reasoning": os.getenv("GRAPH_REASONING_MODEL"),
            "chat": os.getenv("CHAT_MODEL"),
            "document_analysis": os.getenv("DOCUMENT_ANALYSIS_MODEL"),
            "knowledge_extraction": os.getenv("KNOWLEDGE_EXTRACTION_MODEL"),
        }

    def generate(
        self,
        request: LLMRequest,
    ) -> Any:
        model = self._task_to_model.get(request.task)

        if not model:
            raise ValueError(f"No model configured for task: {request.task}")

        return self._hf_client.generate(
            model=model,
            request=request,
        )
