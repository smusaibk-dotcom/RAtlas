import asyncio
from uuid import UUID

from infrastructure.parsers.parse_error_classifier import ParseErrorClassifier
from main import (
    conversation_state_service,
    parse_chunk_tool,
    query_understanding_service,
    search_query_generation_service,
    search_service,
)


async def parse_all(resources):
    semaphore = asyncio.Semaphore(4)

    async def parse(resource):
        async with semaphore:
            print(f"START: {resource.title}")

            try:
                chunks = await parse_chunk_tool.run(
                    resource,
                )

                print(f"DONE : {resource.title}")

                return chunks

            except Exception as e:
                print(f"FAILED: {resource.title}")
                print(e)

                return e

    tasks = [parse(resource) for resource in resources]

    results = await asyncio.gather(
        *tasks,
        return_exceptions=False,
    )

    chunks = []
    failed = []

    for resource, result in zip(resources, results):
        if isinstance(result, Exception):
            failed.append(
                {
                    "resource": resource,
                    "reason": ParseErrorClassifier.classify(result),
                    "message": str(result),
                }
            )

        else:
            chunks.extend(result)

    return chunks, failed


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

    print("QUERY SENT TO LLM:")
    print(query_for_understanding)

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

    resources = []

    for result in search_results:
        resources.extend(result.resources)

    # Parse only the top "n" search results
    max_n_resorcues = 12
    resources = resources[:max_n_resorcues]

    print(f"Parsing {len(resources)} resources...")

    chunks, failed_resources = asyncio.run(parse_all(resources))

    print("=" * 80)
    print("TOTAL PARSED CHUNKS:", len(chunks))
    print("=" * 80)

    return {
        "conversation_id": state.conversation_id,
        "status": understanding.status,
        "understanding": understanding,
        "search_queries": search_queries,
        "search_results": search_results,
        "parsed_chunks": chunks,
        "failed_resources": failed_resources,
    }
