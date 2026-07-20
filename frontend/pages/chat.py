import streamlit as st
from services.query import query_dataset


def chat_screen():

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

    # ---------- Dataset Info ----------

    st.markdown(
        f"""
        <div class="dataset-card">

        <h3>Current Dataset</h3>

        <p><b>Name:</b> {st.session_state.dataset_name}</p>

        <p><b>Business Type:</b> {st.session_state.dataset_type}</p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------- Chat History ----------

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if len(st.session_state.messages) == 0:

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content":
                "Dataset uploaded successfully.\n\n"
                "I'm ready to answer questions about your data."
            }
        )

    # ---------- Display Messages ----------

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # ---------- Chat Input ----------

    question = st.chat_input(
        "Ask anything about your dataset..."
    )

    if question:

        st.session_state.messages.append(
            {
                "role":"user",
                "content":question
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

                answer = data["results"]

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role":"assistant",
                        "content":answer
                    }
                )

                st.write("")

                col1,col2,col3 = st.columns(3)

                with col1:

                    if st.button(
                        "📊 Visualization",
                        key=f"chart_{len(st.session_state.messages)}"
                    ):

                        st.session_state.page="visualization"

                        st.rerun()

                with col2:

                    if st.button(
                        "💡 Insights",
                        key=f"insight_{len(st.session_state.messages)}"
                    ):

                        st.session_state.page="insights"

                        st.rerun()

                with col3:

                    if st.button(
                        "📄 Download Report",
                        key=f"report_{len(st.session_state.messages)}"
                    ):

                        st.session_state.page="report"

                        st.rerun()

            else:

                st.error(response.text)