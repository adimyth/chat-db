import os

import mysql.connector
import requests
import streamlit as st
from cryptography.fernet import Fernet


def get_connections(user_id: str, connection_id: str = None):
    if connection_id is None:
        response = requests.get(
            f"http://localhost:8000/db-connection?user_id={user_id}"
        )
    else:
        response = requests.get(
            f"http://localhost:8000/db-connection?user_id={user_id}&connection_id={connection_id}"
        )
    if response.status_code == 200:
        connections = response.json()
        return connections
    else:
        st.error("Failed to fetch connections.")
        return []


def create_connection(payload):
    response = requests.post(f"http://localhost:8000/db-connection/", json=payload)
    if response.ok:
        st.success("Connection created successfully")
        st.experimental_rerun()
    elif response.status_code == 400:
        st.error(response.json()["detail"])
    else:
        st.error("Failed to create connection")


def update_connection(connection_id, payload):
    response = requests.patch(
        f"http://localhost:8000/db-connection?connection_id={connection_id}",
        json=payload,
    )
    if response.ok:
        st.success("Connection updated successfully")
        del st.session_state.update_id
        st.experimental_rerun()
    elif response.status_code == 400:
        st.error(response.json()["detail"])
    else:
        st.error("Failed to update connection")


def delete_connection(connection_id):
    response = requests.delete(
        f"http://localhost:8000/db-connection?connection_id={connection_id}"
    )
    if response.ok:
        st.success("Connection deleted successfully")
        st.experimental_rerun()
    else:
        st.error("Failed to delete connection")


# fetches a particular chat session from the database given user_id and chat_id
def get_chat_session_history(user_id, connection_id, chat_id):
    response = requests.get(
        f"http://localhost:8000/chat?user_id={user_id}&connection_id={connection_id}&chat_id={chat_id}"
    )
    if response.status_code == 200:
        chat_session = response.json()
        if len(chat_session) == 0:
            st.info("No chat history found.")
            return None
        else:
            return chat_session[0]["chat_history"]
    else:
        st.error("Failed to fetch chat session.")
        return None


def create_chat_session_history(payload):
    response = requests.post(
        f"http://localhost:8000/chat",
        json=payload,
    )
    if response.ok:
        st.success("Chat session created successfully")
        st.experimental_rerun()
    elif response.status_code == 400:
        st.error(response.json()["detail"])
    else:
        st.error("Failed to create chat session")


def update_chat_session_history(chat_id, payload):
    response = requests.patch(
        f"http://localhost:8000/chat?chat_id={chat_id}",
        json=payload,
    )
    if response.ok:
        st.success("Chat session updated successfully")
        st.experimental_rerun()
    elif response.status_code == 400:
        st.error(response.json()["detail"])
    else:
        st.error("Failed to update chat session")


def decrypt_password(token: str) -> str:
    key = os.getenv("SECRET_KEY")
    f = Fernet(key)
    password = f.decrypt(token.encode())
    return password.decode()


def convert_timestamp(timestamp):
    # convert 2023-03-08T15:36:56.931331+00:00 to 2023-03-08 15:36:56
    return timestamp.split(".")[0].replace("T", " ")
