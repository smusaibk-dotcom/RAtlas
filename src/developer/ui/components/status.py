import streamlit as st

from developer.ui.config import STAGES


def status():
    st.subheader("Pipeline Status")

    cols = st.columns(len(STAGES))

    for col, stage in zip(cols, STAGES):
        with col:
            st.info(stage)
