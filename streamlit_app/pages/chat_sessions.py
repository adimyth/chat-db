import webbrowser

import requests
import streamlit as st
from utils import create_chat_session_history


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
    user_chat_sessions = get_user_chats(user_id, connection_id)
    if user_chat_sessions:
        with st.expander("Chat Sessions"):
            for chat in user_chat_sessions:
                chat_title = chat["chat_title"]
                created_at = chat["created_at"]

                cols = st.columns(2)
                # convert to this to href
                cols[1].markdown(f"##### :blue[{created_at}]")
                cols[0].markdown(
                    f"##### [{chat_title}](http://localhost:8501/chat?user_id={user_id}&connection_id={connection_id}&chat_id={chat['chat_id']})",
                    unsafe_allow_html=True,
                )

    else:
        st.info("No chat sessions found.")
        # create a form to create a new chat session which takes in a chat title
        with st.form("create_chat_session"):
            chat_title = st.text_input("Chat title")
            submit = st.form_submit_button("Create chat session")
            if submit:
                payload = {
                    "user_id": user_id,
                    "connection_id": connection_id,
                    "chat_title": chat_title,
                }
                create_chat_session_history(payload)
