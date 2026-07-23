from application.dto.query_understanding_result import (
    QueryUnderstandingResult,
)
from application.services.search_query_generation_service import (
    SearchQueryGenerationService,
)
from infrastructure.adapters.llm_adapter import LLMAdapter
from infrastructure.adapters.search_query_generation_adapter import (
    SearchQueryGenerationAdapter,
)


def main():
    llm = LLMAdapter()

    adapter = SearchQueryGenerationAdapter(llm)

    service = SearchQueryGenerationService(adapter)

    query = QueryUnderstandingResult(
        original_query="Transformers",
        refined_query="Evolution of Transformer models",
        intent="TIMELINE",
        research_domain="Machine Learning",
        confidence_score=0.95,
        status="PROCEED",
    )

    result = service.generate(query)

    print(result.model_dump_json(indent=4))


if __name__ == "__main__":
    main()
