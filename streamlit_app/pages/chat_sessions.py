import os

import requests
import streamlit as st
from dotenv import load_dotenv
from streamlit_supabase_auth import logout_button
from utils import convert_timestamp, create_chat_session_history, get_connections

load_dotenv()


def get_user_chats(user_id, connection_id):
    response = requests.get(
        f"http://localhost:8000/chat?user_id={user_id}&connection_id={connection_id}"
    )
    if response.status_code == 200:
        chats = response.json()
        return chats
    else:
        st.error("Failed to fetch chats.")
        return []


def chat_sessions(user_id: str, connection_id: str):
    st.set_page_config(
        page_title="Chat DB",
        page_icon=":speak_no_evil:",
        initial_sidebar_state="collapsed",
    )

    connection_details = get_connections(user_id, connection_id)
    if len(connection_details) > 0:
        connection_name = connection_details[0]["connection_name"]
        st.title(f":orange[{connection_name}]")

    st.write("###")

    # create a form to create a new chat session which takes in a chat title
    with st.form("create_chat_session", clear_on_submit=True):
        chat_title = st.text_input(
            "Create a new chat session:", placeholder="Chat title, e.g. 'Chat 1'"
        )
        submit = st.form_submit_button("🚀")

    if submit:
        payload = {
            "user_id": user_id,
            "connection_id": connection_id,
            "chat_title": chat_title,
        }
        st.write("Chat session created.")
        create_chat_session_history(payload)

    st.write("###")

    user_chat_sessions = get_user_chats(user_id, connection_id)
    if user_chat_sessions:
        # with st.expander("Chat Sessions"):
        for chat in user_chat_sessions:
            chat_title = chat["chat_title"]
            created_at = convert_timestamp(chat["created_at"])
            chat_id = chat["chat_id"]

            cols = st.columns(2)
            cols[1].markdown(f"##### :orange[{created_at}]")

            url = f"{os.environ.get('APP_URL')}/chat?user_id={user_id}&connection_id={connection_id}&chat_id={chat_id}"
            cols[0].markdown(
                f'#### <a href="{url}" target="_self">{chat_title}</a>',
                unsafe_allow_html=True,
            )

    else:
        st.info("No chat sessions found.")


if __name__ == "__main__":
    user_id = st.experimental_get_query_params()["user_id"][0]
    connection_id = st.experimental_get_query_params()["connection_id"][0]
    chat_sessions(user_id, connection_id)
