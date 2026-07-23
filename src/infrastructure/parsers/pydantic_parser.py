from pydantic import BaseModel

from langchain_core.output_parsers import PydanticOutputParser


class PydanticParser:
    @staticmethod
    def get_parser(response_model: type[BaseModel]) -> PydanticOutputParser:
        return PydanticOutputParser(pydantic_object=response_model)
