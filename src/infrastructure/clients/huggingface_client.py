import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from application.dto.llm_request import LLMRequest
from infrastructure.exceptions.llm_exception import LLMException
from infrastructure.parsers.pydantic_parser import PydanticParser

load_dotenv()


class HuggingFaceClient:
    """Thin wrapper around the Hugging Face Inference API."""

    def __init__(self) -> None:
        self._client = InferenceClient(
            api_key=os.getenv("HF_API_KEY"),
        )

    def generate(
        self,
        model: str,
        request: LLMRequest,
    ):
        try:
            response = self._client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": message.role.value,
                        "content": message.content,
                    }
                    for message in request.messages
                ],
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                top_p=request.top_p,
            )

            if not response.choices:
                raise LLMException("LLM returned no choices.")

            content = response.choices[0].message.content

            if not content:
                raise LLMException("LLM returned an empty response.")

            parser = PydanticParser.get_parser(request.response_model)

            return parser.parse(content)

        except Exception as e:
            raise LLMException(str(e)) from e
