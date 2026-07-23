from main import (
    query_understanding_service,
    search_query_generation_service,
    search_service,
    conversation_state_service,
)

from uuid import UUID


def search(
    query: str,
    conversation_id: UUID | None,
):
    if conversation_id is None:
        state = conversation_state_service.create()
    else:
        state = conversation_state_service.load(conversation_id)

    if state.original_query is None:
        state.original_query = query

    else:
        state.user_clarification = query

    print("STEP 1")

    query_for_understanding = (
        query
        if state.user_clarification is None
        else f"""
    Original Query:
    {state.original_query}

    User Clarification:
    {state.user_clarification}
    """
    )

    understanding = query_understanding_service.analyze(query_for_understanding)

    state.query_understanding = understanding

    conversation_state_service.save(state)

    print("\n========== CONVERSATION STATE ==========")
    print(state.model_dump())
    print("========================================\n")

    print("STEP 2", understanding)

    # ---------------------------------------------------------
    # Stop pipeline if clarification is required
    # ---------------------------------------------------------

    if understanding.status.name == "NEED_CLARIFICATION":
        return {
            "conversation_id": state.conversation_id,
            "status": understanding.status,
            "understanding": understanding,
            "search_queries": None,
            "search_results": None,
        }

    # ---------------------------------------------------------
    # Continue pipeline
    # ---------------------------------------------------------

    search_queries = search_query_generation_service.generate(understanding)

    print("STEP 3", search_queries)

    search_results = search_service.search(search_queries)

    print("STEP 4", search_results)

    return {
        "conversation_id": state.conversation_id,
        "status": understanding.status,
        "understanding": understanding,
        "search_queries": search_queries,
        "search_results": search_results,
    }
