import streamlit as st
from streamlit_chat import message

from response import Response

# Set app title and page layout
st.set_page_config(
    page_title="Streamlit Conversational App", page_icon=":speak_no_evil:"
)

# Set app header with title
st.header("Streamlit Conversational App")

# Initialising the response class
response = Response()
tables = response.get_table_names()
table = st.selectbox("Choose data to query against:", tables)

st.title("ChatGPT-like Web App")

# storing the chat
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []

# get user input
user_input = st.text_input("You:", key="input")

# generate response
if user_input:
    output = response.generate_response(user_input)
    # store the output
    st.session_state["past"].append(user_input)
    st.session_state["generated"].append(output)
if st.session_state["generated"]:
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
