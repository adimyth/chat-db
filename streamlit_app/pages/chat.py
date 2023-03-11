import random
import string
import time
from datetime import datetime
from decimal import Decimal

import streamlit as st
from model_response import ModelResponse
from streamlit_chat import message
from utils import (
    decrypt_password,
    get_chat_session_history,
    get_connections,
    update_chat_session_history,
)


# save session chat history
def save_session(user_id, connection_id, chat_id):
    payload = {}
    payload["chat_history"] = {}

    # new chat session
    for i in range(len(st.session_state["generated"])):
        payload["chat_history"][str(int(time.time()))] = {
            "ai": st.session_state["generated"][i],
            user_id: st.session_state["past"][i],
            "timestamp": st.session_state["timestamp"],
        }
    payload["updated_at"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # update chat history
    update_chat_session_history(
        chat_id,
        payload,
    )
    st.experimental_rerun()


# TODO: check why when clicking on save session button, the existing chat session is printed twice?
def chat_app():
    # Set page configs
    st.set_page_config(
        page_title="Chat DB",
        page_icon=":speak_no_evil:",
        initial_sidebar_state="collapsed",
    )
    st.title(":orange[Chat DB]")

    # fetch user_id, connection_id and chat_id from the query params
    user_id = st.experimental_get_query_params()["user_id"][0]
    connection_id = st.experimental_get_query_params()["connection_id"][0]
    chat_id = st.experimental_get_query_params()["chat_id"][0]

    # fetch connection details
    connection_details = get_connections(user_id, connection_id)
    if len(connection_details) > 0:
        connection_type = connection_details[0]["connection_type"]
        db_host = connection_details[0]["db_host"]
        db_port = connection_details[0]["db_port"]
        db_name = connection_details[0]["db_name"]
        db_username = connection_details[0]["db_username"]
        db_encrypted_password = connection_details[0]["db_encrypted_password"]
        db_password = decrypt_password(db_encrypted_password)

    # initialising the response class
    response = ModelResponse(
        connection_type, db_host, db_port, db_name, db_username, db_password
    )
    tables = response.get_table_names()
    table = st.selectbox("Choose data to query against:", tables)
    response.create_index(table)

    # initialise session state
    if "generated" not in st.session_state:
        st.session_state["generated"] = []
    if "past" not in st.session_state:
        st.session_state["past"] = []

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area("", key="input")
        submit_button = st.form_submit_button(label="Submit")

    # add a button to save the session
    if st.button("Save Session"):
        save_session(user_id, connection_id, chat_id)

    # fetch & display chat history
    messages = []
    chat_history = get_chat_session_history(user_id, connection_id, chat_id)
    if chat_history and len(chat_history) > 0:
        for key, value in chat_history.items():
            messages.append(message(value[user_id], is_user=True, key=key + "_user"))
            messages.append(message(value["ai"], key=key))
            st.write("---")

    # generate ai response
    if submit_button:
        output = response.generate_response(user_input)
        # store the output
        st.session_state["past"].append(user_input)
        st.session_state["generated"].append(output)
        st.session_state["timestamp"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    if st.session_state["generated"]:
        for i in range(len(st.session_state["generated"]) - 1, -1, -1):
            key = "".join(random.choices(string.ascii_letters, k=7))
            messages.append(
                message(st.session_state["past"][i], is_user=True, key=f"{key}_user")
            )
            messages.append(message(st.session_state["generated"][i], key=key))
            st.write("---")


if __name__ == "__main__":
    chat_app()
