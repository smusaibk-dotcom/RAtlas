from infrastructure.adapters.llm_adapter import LLMAdapter
from application.dto.llm_request import LLMRequest
from application.dto.llm_message import LLMMessage, MessageRole
from typing import Any
from application.dto.query_understanding_result import QueryUnderstandingResult


def main():
    llm = LLMAdapter()

    request = LLMRequest(
        task="query_understanding",
        messages=[
            LLMMessage(
                role=MessageRole.SYSTEM,
                content="You are a helpful assistant.",
            ),
            LLMMessage(
                role=MessageRole.USER,
                content="Reply with exactly: Hello Ratlas",
            ),
        ],
        response_model=QueryUnderstandingResult,
        temperature=0.0,
    )

    response = llm.generate(request)

    print("\n===== RESPONSE =====\n")
    print(response)


if __name__ == "__main__":
    main()
