import streamlit as st
from utils.session import logout


def dashboard_screen():

    st.markdown(
        """
        <style>

        .stApp{
            background:#0F172A;
        }

        h1,h2,h3{
            color:white;
        }

        p{
            color:#CBD5E1;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # ---------------- Header ---------------- #

    col1, col2 = st.columns([8,2])

    with col1:
        st.markdown(
            "<h1 style='color:#2563EB;'>AI Data Analyst</h1>",
            unsafe_allow_html=True
        )

    with col2:
        if st.button("Logout", use_container_width=True):
            logout()

    st.divider()

    st.markdown("# Welcome Back 👋")
    st.write(
        "Analyze datasets using AI-powered agents, SQL generation, business insights, charts and downloadable reports."
    )

    st.write("")

    # ---------------- Metrics ---------------- #

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Datasets", 0)
    c2.metric("Queries", 0)
    c3.metric("Reports", 0)
    c4.metric("Charts", 0)

    st.write("")
    st.write("")

    st.markdown("## AI Workspace")

    # ---------------- First Row ---------------- #

    col1, col2, col3 = st.columns(3)

    with col1:

        with st.container(border=True):

            st.subheader("📤 Upload Dataset")

            st.write(
                "Upload CSV files and let AI clean and understand your data."
            )

            if st.button("Open Upload", use_container_width=True):
                st.session_state.page = "upload"
                st.rerun()

    with col2:

        with st.container(border=True):

            st.subheader("🤖 SQL Agent")

            st.write(
                "Ask questions about your dataset in natural language."
            )

            if st.button("Open SQL Chat", use_container_width=True):
                st.session_state.page = "sql_chat"
                st.rerun()

    with col3:

        with st.container(border=True):

            st.subheader("📊 Visualization")

            st.write(
                "Automatically create interactive charts."
            )

            if st.button("Open Charts", use_container_width=True):
                st.session_state.page = "visualization"
                st.rerun()

    st.write("")

    # ---------------- Second Row ---------------- #

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.subheader("💡 Insight Agent")

            st.write(
                "Generate AI-powered insights and recommendations."
            )

            if st.button("View Insights", use_container_width=True):
                st.session_state.page = "insights"
                st.rerun()

    with col2:

        with st.container(border=True):

            st.subheader("📄 Report Generator")

            st.write(
                "Generate professional PDF reports."
            )

            if st.button("Generate Report", use_container_width=True):
                st.session_state.page = "reports"
                st.rerun()

    st.write("")
    st.info("Upload a dataset to unlock all AI agents.")