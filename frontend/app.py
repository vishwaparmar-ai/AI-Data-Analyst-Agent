import streamlit as st

from pages.login import login_screen
from pages.register import register_screen
from pages.dashboard import dashboard_screen
from pages.upload import upload_screen
from pages.chat import chat_screen
from pages.visualization import visualization_screen


st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Hide Streamlit UI
st.markdown("""
<style>

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

[data-testid="stSidebar"]{
display:none;
}

</style>

""", unsafe_allow_html=True)


# Session

if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "token" not in st.session_state:
    st.session_state.token = None



# Routing

if not st.session_state.logged_in:

    if st.session_state.page == "login":

        login_screen()

    elif st.session_state.page == "register":
        register_screen()


else:

    if st.session_state.page == "dashboard":
        dashboard_screen()
    if st.session_state.page == "upload":
        upload_screen()
    if st.session_state.page == "chat":
        chat_screen()

        st.write("Current Page:", st.session_state.page)
    if st.session_state.page == "visualization":
        visualization_screen()