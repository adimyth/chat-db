import os

import streamlit as st
from dotenv import load_dotenv
from pages.connection import connections_app
from streamlit_supabase_auth import login_form, logout_button

load_dotenv()


def login():
    st.set_page_config(
        page_title="Chat DB",
        page_icon=":speak_no_evil:",
        initial_sidebar_state="collapsed",
    )

    session = login_form(
        url=os.getenv("SUPABASE_URL"),
        apiKey=os.getenv("SUPABASE_KEY"),
        # Social logins are not working. Refer - https://github.com/sweatybridge/streamlit-supabase-auth/issues/15
        # providers=["google", "github"],
    )

    if session:
        with st.sidebar:
            st.write(f"Welcome {session['user']['email']}")
            logout_button()
        connections_app(session["user"]["id"])


if __name__ == "__main__":
    login()
