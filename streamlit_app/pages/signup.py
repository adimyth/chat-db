import os

import streamlit as st
from connection import connections_app
from dotenv import load_dotenv
from streamlit_supabase_auth import login_form, logout_button

load_dotenv()


def login():
    session = login_form(
        url=os.getenv("SUPABASE_URL"),
        apiKey=os.getenv("SUPABASE_KEY"),
        providers=["google", "github"],
    )

    if session:
        st.experimental_set_query_params(page=["success"])
        with st.sidebar:
            st.write(f"Welcome {session['user']['email']}")
            logout_button()
        connections_app()


if __name__ == "__main__":
    login()
