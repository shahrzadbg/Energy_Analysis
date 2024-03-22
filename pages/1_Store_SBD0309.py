from modules.security import check_password
import streamlit as st
from modules.header import headings
from modules.utils import description

# if not check_password():
#     st.stop()

headings()

description(
        "In this section you will see a full report of energy analysis for the store SBD0309."
    )



view_option = st.sidebar.selectbox(
    "view:",
    ["monthly", "yearly"],
    key="home_view_option",
)

