from application.coordinators.coordinator_agent import CoordinatorAgent
from application.services.query_understanding_service import (
    QueryUnderstandingService,
)
from application.services.search_query_generation_service import (
    SearchQueryGenerationService,
)
from application.services.search_service import SearchService
from infrastructure.adapters.llm_adapter import LLMAdapter
from infrastructure.adapters.query_understanding_adapter import (
    QueryUnderstandingAdapter,
)
from infrastructure.adapters.search_adapter import SearchAdapter
from infrastructure.adapters.search_query_generation_adapter import (
    SearchQueryGenerationAdapter,
)


def main():
    # Shared LLM
    llm = LLMAdapter()

    # Query Understanding
    query_understanding_adapter = QueryUnderstandingAdapter(llm)
    query_understanding_service = QueryUnderstandingService(query_understanding_adapter)

    # Search Query Generation
    search_query_generation_adapter = SearchQueryGenerationAdapter(llm)
    search_query_generation_service = SearchQueryGenerationService(search_query_generation_adapter)

    # Search
    search_adapter = SearchAdapter()
    search_service = SearchService(search_adapter)

    # Coordinator
    coordinator = CoordinatorAgent(
        query_understanding_service=query_understanding_service,
        search_query_generation_service=search_query_generation_service,
        search_service=search_service,
    )

    result = coordinator.start_research("How did Transformers evolve?")

    print(result.model_dump_json(indent=4))


if __name__ == "__main__":
    main()
