import streamlit as st

st.set_page_config(
    page_title="Ratlas - Search Debug",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 Search Stage")

st.divider()

# ==========================
# Query
# ==========================

query = st.text_input(
    "Research Query",
    placeholder="Vision Transformer",
)

search_clicked = st.button(
    "Search",
    width="stretch",
)

st.divider()

# ==========================
# Generated Queries
# ==========================

st.subheader("Generated Search Queries")

generated_queries_placeholder = st.empty()

st.divider()

# ==========================
# Metrics
# ==========================

st.subheader("Search Metrics")

c1, c2, c3, c4 = st.columns(4)

with c1:
    total_queries_metric = st.empty()

with c2:
    requested_metric = st.empty()

with c3:
    retrieved_metric = st.empty()

with c4:
    response_time_metric = st.empty()

c5, c6, c7, c8 = st.columns(4)

with c5:
    pdf_metric = st.empty()

with c6:
    html_metric = st.empty()

with c7:
    youtube_metric = st.empty()

with c8:
    duplicate_metric = st.empty()

st.divider()

# ==========================
# Providers
# ==========================

st.subheader("Providers")

providers_placeholder = st.empty()

st.divider()

# ==========================
# Resources
# ==========================

st.subheader("Resources")

resources_placeholder = st.empty()

st.divider()

# ==========================
# Logs
# ==========================

st.subheader("Logs")

logs_placeholder = st.empty()

st.divider()

# ==========================
# Raw JSON
# ==========================

with st.expander("Raw Search Output"):
    raw_placeholder = st.empty()


# ==========================================================
# TEMPORARY DEMO DATA
# Remove once SearchService is connected
# ==========================================================

if search_clicked and query:
    from developer.ui.api import search

    result = search(query)

    generated_queries_placeholder.json(result["search_queries"].model_dump())

    raw_placeholder.json(
        result["search_results"],
    )

    total_queries_metric.metric(
        "Queries",
        3,
    )

    requested_metric.metric(
        "Requested",
        30,
    )

    retrieved_metric.metric(
        "Retrieved",
        26,
    )

    response_time_metric.metric(
        "Time",
        "2.41 s",
    )

    pdf_metric.metric(
        "PDF",
        15,
    )

    html_metric.metric(
        "HTML",
        8,
    )

    youtube_metric.metric(
        "YouTube",
        3,
    )

    duplicate_metric.metric(
        "Duplicates",
        2,
    )

    providers_placeholder.json({"Semantic Scholar": 12, "Arxiv": 8, "Google": 6})

    resources_placeholder.dataframe(
        [
            {
                "Type": "PDF",
                "Title": "Attention Is All You Need",
                "Provider": "Arxiv",
                "URL": "https://...",
            },
            {
                "Type": "HTML",
                "Title": "HuggingFace Blog",
                "Provider": "Google",
                "URL": "https://...",
            },
        ]
    )

    logs_placeholder.code("""

Searching Semantic Scholar...

Searching Arxiv...

Searching Google...

Finished.

""")

    raw_placeholder.json({"status": "success"})
