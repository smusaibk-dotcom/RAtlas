from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel


class PydanticParser:
    @staticmethod
    def get_parser(response_model: type[BaseModel]) -> PydanticOutputParser:
        return PydanticOutputParser(pydantic_object=response_model)
