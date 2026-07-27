from collections import Counter

import streamlit as st

from application.dto.query_understanding_result import QueryUnderstandingStatus
from developer.collectors.search_colector import SearchCollector
from developer.ui.api import search
from developer.ui.components.status import status


def dashboard():
    st.title("😊 Ratlas Developer Console")
    st.caption("Internal Debug Interface")

    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = None

    if "search_result" not in st.session_state:
        st.session_state.search_result = None

    if "search_debug" not in st.session_state:
        st.session_state.search_debug = None

    if "parsed_chunks" not in st.session_state:
        st.session_state.parsed_chunks = []

    if "failed_resources" not in st.session_state:
        st.session_state.failed_resources = []

    st.divider()

    query = st.text_input(
        "Research Topic",
        placeholder="Transformers",
    )

    run = st.button(
        "Run Pipeline",
        width="stretch",
    )

    # -------------------------------------------------
    # Execute Backend
    # -------------------------------------------------

    result = st.session_state.search_result
    debug = st.session_state.search_debug

    if run and query:
        result = search(
            query=query,
            conversation_id=st.session_state.conversation_id,
        )

        # Store conversation ID only once
        if st.session_state.conversation_id is None:
            st.session_state.conversation_id = result["conversation_id"]

        # Handle clarification requests
        if result["understanding"].status == QueryUnderstandingStatus.NEED_CLARIFICATION:
            st.warning(result["understanding"].clarification_message)

            st.write(result["understanding"].clarification_options)

            return

        # Store parsed output
        st.session_state["parsed_chunks"] = result["parsed_chunks"]
        st.session_state["failed_resources"] = result["failed_resources"]

        # Always collect debug information after a successful search
        debug = SearchCollector.collect(result["search_results"])

        st.session_state.search_result = result
        st.session_state.search_debug = debug

    st.divider()

    status()

    st.divider()

    left, right = st.columns([3, 1])

    # -------------------------------------------------
    # Output
    # -------------------------------------------------

    with left:
        st.subheader("Output")

        if result:
            st.json(
                {
                    "understanding": result["understanding"].model_dump(),
                    "search_queries": result["search_queries"].model_dump(),
                }
            )

        else:
            st.code(
                "Nothing executed.",
                language="text",
            )

    # -------------------------------------------------
    # Metrics
    # -------------------------------------------------

    with right:
        st.subheader("Metrics")

        if debug:
            st.metric("Queries", debug["query_count"])
            st.metric("Requested", debug["requested_results"])
            st.metric("Retrieved", debug["retrieved_results"])
            st.metric("Resources", debug["unique_resources"])

        else:
            st.metric("Queries", 0)
            st.metric("Requested", 0)
            st.metric("Retrieved", 0)
            st.metric("Resources", 0)

    st.divider()

    # -------------------------------------------------
    # Logs
    # -------------------------------------------------

    st.subheader("Logs")

    if debug:
        st.code(
            "\n".join(debug["logs"]),
            language="text",
        )

    else:
        st.code(
            "Waiting for execution...",
            language="text",
        )

    st.divider()

    # -------------------------------------------------
    # Search Statistics
    # -------------------------------------------------

    if debug:
        st.subheader("Search Statistics")

        st.divider()

        failure_counter = Counter(failure["reason"].value for failure in result["failed_resources"])

        st.subheader("Parsing Statistics")

        st.json(
            {
                "parsed_resources": len(debug["resources"]) - len(result["failed_resources"]),
                "failed_resources": len(result["failed_resources"]),
                "generated_chunks": len(result["parsed_chunks"]),
                "failures": dict(failure_counter),
            }
        )

        st.json(
            {
                "providers": debug["providers"],
                "pdf": debug["pdf_count"],
                "html": debug["html_count"],
                "youtube": debug["youtube_count"],
                "duplicates": debug["duplicate_resources"],
                "elapsed_time": debug["elapsed_time"],
            }
        )

        st.divider()

        # -------------------------------------------------
        # Resources
        # -------------------------------------------------

        st.subheader("Resources")

        for i, resource in enumerate(debug["resources"]):
            with st.expander(f"{str(resource.resource_type).upper()} | {resource.title}"):
                c1, c2 = st.columns([5, 1])

                with c1:
                    st.write(f"**Provider:** {resource.provider}")
                    score = (
                        f"{resource.relevance_score:.3f}"
                        if resource.relevance_score is not None
                        else "-"
                    )

                    st.write(f"**Score:** {score}")

                    st.code(resource.url)

                with c2:
                    st.success("✓ Parsed")

        st.success("Search completed.")
