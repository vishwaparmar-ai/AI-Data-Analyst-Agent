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

        if question == "":

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

        st.subheader("Chart Description")

        st.write(data["chart_plan"])

        chart_path = data["chart_path"]

        image_url = f"{BASE_URL}/{chart_path}"

        st.write(image_url)      # temporary for debugging

        st.image(
            image_url,
            caption="Generated Visualization",
            use_container_width=True
        )

        st.image(
            image_url,
            caption="Generated Visualization",
            use_container_width=True
        )

    st.write("")

    if st.button(
        "← Back to Chat",
        use_container_width=True
    ):

        st.session_state.page = "chat"

        st.rerun()