import streamlit as st

from streamlit_option_menu import option_menu

from developer.ui.config import SIDEBAR_TITLE


def sidebar():
    with st.sidebar:
        page = option_menu(
            SIDEBAR_TITLE,
            ["Dashboard", "Search", "Download", "Parser", "Chunking", "KEE", "Timeline", "Logs"],
            icons=[
                "speedometer2",
                "search",
                "cloud-download",
                "file-earmark-text",
                "grid",
                "diagram-3",
                "share",
                "terminal",
            ],
            default_index=0,
        )

    return page
