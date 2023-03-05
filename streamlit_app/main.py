import streamlit as st
from dotenv import load_dotenv
from streamlit_chat import message

from response import Response

# Set app title and page layout
st.set_page_config(page_title="Chat DB", page_icon=":speak_no_evil:")

# Set app title
st.title("Chat DB")

# Initialising the response class
response = Response()
tables = response.get_table_names()
table = st.selectbox("Choose data to query against:", tables)

# Create index
response.create_index(table)

# Initialise session state
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []


# Clear session state
def clear_form():
    st.session_state["input"] = ""


with st.form("chat_form"):
    # Get user input
    user_input = st.text_area("You:", key="input")
    # Add submit button
    submit_button = st.form_submit_button(label="Submit")
    clear_button = st.form_submit_button(label="Clear", on_click=clear_form)


# Generate response
if submit_button:
    output = response.generate_response(user_input)
    # store the output
    st.session_state["past"].append(user_input)
    st.session_state["generated"].append(output)

if st.session_state["generated"]:
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
