import streamlit as st


def headings():
    st.markdown(
        f"<h1>Staples Canada</h1>", unsafe_allow_html=True
    )
    st.markdown(
        f"<h2>Energy Analysis Report</h2>",
        unsafe_allow_html=True,
    )
    st.caption(
        "This report is provided by Enerfrog Business Services. © 2023 Enerfrog - www.enerfrog.com"
    )
    st.divider()