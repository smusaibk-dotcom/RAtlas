from infrastructure.adapters.llm_adapter import LLMAdapter

from infrastructure.adapters.query_understanding_adapter import (
    QueryUnderstandingAdapter,
)
from infrastructure.adapters.search_query_generation_adapter import (
    SearchQueryGenerationAdapter,
)
from infrastructure.adapters.search_adapter import SearchAdapter

from application.services.query_understanding_service import (
    QueryUnderstandingService,
)
from application.services.search_query_generation_service import (
    SearchQueryGenerationService,
)
from application.services.search_service import SearchService

from infrastructure.adapters.conversation_state_adapter import (
    ConversationStateAdapter,
)

from application.services.conversation_state_service import (
    ConversationStateService,
)


conversation_state_service = ConversationStateService(ConversationStateAdapter())

llm = LLMAdapter()

query_understanding_service = QueryUnderstandingService(QueryUnderstandingAdapter(llm))

search_query_generation_service = SearchQueryGenerationService(SearchQueryGenerationAdapter(llm))

search_service = SearchService(SearchAdapter())
