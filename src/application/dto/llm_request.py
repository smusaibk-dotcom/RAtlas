from typing import Any

from pydantic import BaseModel, Field

from application.dto.llm_message import LLMMessage


class LLMRequest(BaseModel):
    task: str

    messages: list[LLMMessage]

    response_model: type[BaseModel]

    temperature: float = Field(default=0.0, ge=0.0, le=2.0)

    max_tokens: int = Field(default=2048, gt=0)

    top_p: float = Field(default=1.0, gt=0.0, le=1.0)

    stream: bool = False
