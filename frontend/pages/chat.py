import streamlit as st

from services.query import query_dataset


def chat_screen():

    # ---------------- CSS ---------------- #

    st.markdown("""
    <style>

    .stApp{
        background:#0F172A;
    }

    .dataset-card{
        background:#1E293B;
        padding:20px;
        border-radius:12px;
        border:1px solid #2563EB;
        margin-bottom:20px;
    }

    .dataset-card h3{
        color:white;
        margin-bottom:10px;
    }

    .dataset-card p{
        color:#CBD5E1;
        margin:4px 0;
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------------- Session ---------------- #

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "show_actions" not in st.session_state:
        st.session_state.show_actions = False

    if "last_question" not in st.session_state:
        st.session_state.last_question = ""

    # ---------------- Dataset Card ---------------- #

    st.markdown(
        f"""
        <div class="dataset-card">

        <h3>Current Dataset</h3>

        <p><b>Name:</b> {st.session_state.get("dataset_name","")}</p>

        <p><b>Business Type:</b> {st.session_state.get("dataset_type","")}</p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------- Welcome Message ---------------- #

    if len(st.session_state.messages) == 0:

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content":
                "Dataset uploaded successfully.\n\n"
                "Ask me anything about your data."
            }
        )

    # ---------------- Display Chat ---------------- #

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # ---------------- User Question ---------------- #

    question = st.chat_input(
        "Ask anything about your dataset..."
    )

    if question:

        st.session_state.last_question = question

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):

            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                response = query_dataset(
                    token=st.session_state.token,
                    dataset_id=st.session_state.dataset_id,
                    question=question
                )

            if response.status_code == 200:

                data = response.json()

                # Change this key if your backend returns something different
                answer = data["results"]

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

                st.session_state.show_actions = True

            else:

                st.error(response.text)

    # ---------------- Action Buttons ---------------- #

    if st.session_state.show_actions:

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:

            if st.button(
                "📊 Visualization",
                use_container_width=True
            ):

                st.session_state.page = "visualization"

                st.rerun()

        with col2:

            if st.button(
                "💡 Insights",
                use_container_width=True
            ):

                st.session_state.page = "insights"

                st.rerun()

        with col3:

            if st.button(
                "📄 Download Report",
                use_container_width=True
            ):

                st.session_state.page = "report"

                st.rerun()