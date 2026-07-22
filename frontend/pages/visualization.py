import streamlit as st

from services.visualization import generate_visualization

BASE_URL = "http://127.0.0.1:8000"


def visualization_screen():

    st.title("📊 AI Visualization")

    st.write(
        "Describe the chart you would like to generate."
    )

    question = st.text_input(
        "Visualization Request",
        placeholder="Example: Show sales by category"
    )

    if st.button(
        "Generate Visualization",
        use_container_width=True
    ):

        if not question.strip():

            st.warning(
                "Please enter a visualization request."
            )
            st.stop()

        with st.spinner("Generating visualization..."):

            response = generate_visualization(
                token=st.session_state.token,
                dataset_id=st.session_state.dataset_id,
                question=question
            )

        if response.status_code != 200:

            st.error(response.text)
            st.stop()

        data = response.json()

        st.success("Visualization generated successfully.")

        # ---------------- Chart Title ---------------- #

        st.markdown(
            f"### {data['chart_plan']['title']}"
        )

        # ---------------- Chart Image ---------------- #

        chart_path = data["chart_path"].replace("\\", "/")

        image_url = f"{BASE_URL}/{chart_path}"

        col1, col2, col3 = st.columns([1, 4, 1])

        with col2:

            st.image(
                image_url,
                width=960
            )

    st.write("")

    if st.button(
        "← Back to Chat",
        use_container_width=True
    ):

        st.session_state.page = "chat"

        st.rerun()