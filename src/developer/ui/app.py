import streamlit as st

from developer.ui.components.sidebar import sidebar
from developer.ui.config import *
from developer.ui.pages.dashboard import dashboard

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=LAYOUT)

with open("src/developer/ui/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


page = sidebar()


if page == "Dashboard":
    dashboard()

else:
    st.title(page)

    st.info("Coming in next parts.")
