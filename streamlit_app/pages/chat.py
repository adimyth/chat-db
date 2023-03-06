import streamlit as st
from datetime import datetime
from response import Response
from streamlit_chat import message
from utils import (
    get_chat_session_history,
    update_chat_session_history,
    create_chat_session_history,
)


# clear form input
def clear_form():
    st.session_state["input"] = ""


def chat_app():
    # Set app title
    st.title("Chat DB")

    # fetch user_id, connection_id and chat_id from the query params
    user_id = st.experimental_get_query_params()["user_id"][0]
    connection_id = st.experimental_get_query_params()["connection_id"][0]
    chat_id = st.experimental_get_query_params()["chat_id"][0]

    # initialising the response class
    response = Response()
    tables = response.get_table_names()
    table = st.selectbox("Choose data to query against:", tables)

    # create table content index
    response.create_index(table)

    # initialise session state
    if "generated" not in st.session_state:
        st.session_state["generated"] = []
    if "past" not in st.session_state:
        st.session_state["past"] = []

    # fetch & display chat history
    messages = []
    chat_history = get_chat_session_history(user_id, connection_id, chat_id)
    st.write(chat_history)
    if len(chat_history) > 0:
        for key, value in chat_history.items():
            messages.append(message(value["username"], is_user=True, key=key + "_user"))
            messages.append(message(value["ai"], key=key))

    with st.form("chat_form"):
        user_input = st.text_area("You:", key="input")
        submit_button = st.form_submit_button(label="Submit")
        st.form_submit_button(label="Clear", on_click=clear_form)

    # generate ai response
    if submit_button:
        output = response.generate_response(user_input)
        # store the output
        st.session_state["past"].append(user_input)
        st.session_state["generated"].append(output)
        st.session_state["timestamp"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    if st.session_state["generated"]:
        for i in range(len(st.session_state["generated"]) - 1, -1, -1):
            messages.append(
                message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
            )
            messages.append(message(st.session_state["generated"][i], key=str(i)))

        payload = {}
        for i in range(len(st.session_state["generated"])):
            payload[str(i + 1)] = {
                "ai": st.session_state["generated"][i],
                user_id: st.session_state["past"][i],
                "timestamp": st.session_state["timestamp"],
            }

        # update chat history
        update_chat_session_history(
            user_id,
            connection_id,
            chat_id,
            payload,
        )


if __name__ == "__main__":
    chat_app()
