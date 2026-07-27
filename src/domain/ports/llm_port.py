from abc import ABC, abstractmethod
from typing import Any

from application.dto.llm_request import LLMRequest


class LLMPort(ABC):
    @abstractmethod
    def generate(
        self,
        request: LLMRequest,
    ) -> Any:
        """
        Generate a structured response from an LLM.
        """
        raise NotImplementedError
