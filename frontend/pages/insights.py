import streamlit as st

from services.insights import generate_insights


def insights_screen():

    st.title("💡 AI Business Insights")

    st.write(
        "Generate AI-powered business insights and recommendations from your dataset."
    )

    if st.button(
        "Generate Insights",
        use_container_width=True
    ):

        with st.spinner("Analyzing dataset..."):

            response = generate_insights(
                token=st.session_state.token,
                dataset_id=st.session_state.dataset_id
            )

        if response.status_code != 200:

            st.error(response.text)
            st.stop()

        data = response.json()

        st.success("Insights generated successfully.")

        # -------------------------------
        # Dataset Information
        # -------------------------------

        st.markdown("## 📁 Dataset")

        col1, col2 = st.columns(2)

        with col1:
            st.info(f"**Dataset ID**\n\n{data['dataset_id']}")

        with col2:
            st.info(f"**Business Type**\n\n{data['dataset_type']}")

        st.divider()

        # -------------------------------
        # Business Summary
        # -------------------------------

        st.markdown("## 📖 Business Summary")

        st.write(data["business_summary"])

        st.divider()

        # -------------------------------
        # Executive Summary
        # -------------------------------

        st.markdown("## 📋 Executive Summary")

        st.write(data["executive_summary"])

        st.divider()

        # -------------------------------
        # Insights
        # -------------------------------

        st.markdown("## 💡 Key Insights")

        for insight in data["insights"]:

            st.success(insight)

        st.divider()

        # -------------------------------
        # Recommendations
        # -------------------------------

        st.markdown("## 🚀 Recommendations")

        for recommendation in data["recommendations"]:

            st.info(recommendation)

    st.write("")

    if st.button(
        "← Back to Chat",
        use_container_width=True
    ):

        st.session_state.page = "chat"

        st.rerun()