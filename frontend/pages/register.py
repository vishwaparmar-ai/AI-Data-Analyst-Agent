import streamlit as st
from services.auth import register


def register_screen():

    # ---------------- CSS ---------------- #

    st.markdown("""
    <style>

    .stApp{
        background-color:#0F172A;
    }

    h1{
        color:white;
        text-align:center;
        margin-bottom:0px;
    }

    h4{
        color:#60A5FA;
        text-align:center;
        margin-bottom:35px;
    }

    div[data-testid="stTextInput"] input{
        border-radius:10px;
        border:1px solid #2563EB;
        background:#1E293B;
        color:white;
    }

    div[data-testid="stButton"] button{
        background:#2563EB;
        color:white;
        border:none;
        border-radius:10px;
        height:45px;
        font-weight:600;
    }

    div[data-testid="stButton"] button:hover{
        background:#1D4ED8;
        color:white;
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------------- Heading ---------------- #

    st.markdown("<h1>Create Account</h1>", unsafe_allow_html=True)
    st.markdown("<h4>Register to continue</h4>", unsafe_allow_html=True)

    # ---------------- Center Form ---------------- #

    left, center, right = st.columns([2, 1.5, 2])

    with center:

        username = st.text_input(
            "Username",
            placeholder="Enter your username"
        )

        email = st.text_input(
            "Email",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            placeholder="Enter your password",
            type="password"
        )

        st.write("")

        if st.button("Create Account", use_container_width=True):

            if not username or not email or not password:

                st.warning("Please fill all fields.")

            else:

                response = register(
                    username=username,
                    email=email,
                    password=password
                )

                if response.status_code in [200,201]:

                    st.success("Account created successfully!")

                    st.session_state.page = "login"

                    st.rerun()

                else:

                    try:
                        error = response.json()["detail"]
                    except Exception:
                        error = "Registration failed."

                    st.error(error)


     