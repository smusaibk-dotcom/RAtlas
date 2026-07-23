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

    result = None
    debug = None

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

        # Always collect debug information after a successful search
        debug = SearchCollector.collect(result["search_results"])

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

        st.dataframe(
            [
                {
                    "Title": r.title,
                    "Provider": r.provider,
                    "URL": r.url,
                    "Score": r.relevance_score,
                }
                for r in debug["resources"]
            ],
            width="stretch",
        )

        st.success("Search completed.")
