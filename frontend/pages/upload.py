import streamlit as st

from services.upload import upload_dataset


def upload_screen():

    st.markdown("""
    <style>

    .stApp{
        background:#0F172A;
    }

    h1{
        color:white;
        text-align:center;
    }

    p{
        color:#CBD5E1;
        text-align:center;
    }

    div[data-testid="stFileUploader"]{
        border:2px dashed #2563EB;
        border-radius:12px;
        padding:20px;
    }

    div[data-testid="stButton"] button{
        background:#2563EB;
        color:white;
        height:45px;
        border-radius:8px;
        border:none;
        font-weight:bold;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1>Upload Dataset</h1>", unsafe_allow_html=True)

    st.markdown(
        "<p>Select a CSV file to begin AI analysis.</p>",
        unsafe_allow_html=True
    )

    st.write("")

    left, center, right = st.columns([1.5,2,1.5])

    with center:

        uploaded_file = st.file_uploader(
            "Choose CSV Dataset",
            type=["csv"]
        )

        st.write("")

        if st.button(
            "Upload Dataset",
            use_container_width=True
        ):

            if uploaded_file is None:

                st.warning("Please choose a CSV file.")

                st.stop()

            with st.spinner("Uploading dataset..."):

                response = upload_dataset(
                    uploaded_file,
                    st.session_state.token
                )

            if response.status_code != 200:

                st.error(response.text)

                st.stop()

            data = response.json()

            st.success("Dataset uploaded successfully.")

            # Save for future pages

            st.session_state.dataset_id = data["dataset_id"]

            st.session_state.page = "chat"

            st.session_state.dataset_name = data["dataset_name"]

            st.session_state.dataset_type = data["dataset_type"]

            st.rerun()

        st.write("")

        