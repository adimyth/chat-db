import streamlit as st
from dotenv import load_dotenv
from pages.chat_sessions import chat_sessions
from utils import (create_connection, delete_connection, get_connections,
                   update_connection)

load_dotenv()


def connections_app(user_id):
    st.title(":green[Connections]")
    create_new_connection(user_id)
    st.write("###")
    modify_existing_connections(user_id=user_id)


def create_new_connection(user_id):
    st.header(":orange[Create Connection]")

    with st.expander("Create a new connection"):
        with st.form(key="connection_form", clear_on_submit=True):
            connection_name = st.text_input(label="Connection Name")
            connection_type = st.selectbox(
                label="Connection Type", options=["postgres", "mysql"]
            )
            db_host = st.text_input(label="DB Host")
            db_port = st.text_input(label="DB Port")
            db_name = st.text_input(label="DB Name")
            db_user = st.text_input(label="DB User")
            db_password = st.text_input(label="DB Password", type="password")

            if st.form_submit_button(label="🚀"):
                st.write("Creating connection")

                payload = {
                    "connection_name": connection_name,
                    "connection_type": connection_type,
                    "db_host": db_host,
                    "db_port": db_port,
                    "db_name": db_name,
                    "db_username": db_user,
                    "db_password": db_password,
                    "user_id": user_id,
                }
                create_connection(payload)


def modify_existing_connections(user_id):
    st.header(":orange[Existing Connections]")
    connections = get_connections(user_id=user_id)
    if connections:
        # cols = st.columns(4)
        # cols[0].markdown("#### Name")
        # cols[1].markdown("#### Type")
        # cols[2].markdown("#### Update")
        # cols[3].markdown("#### Delete")

        st.write("---")
        for connection in connections:
            connection_id = connection["connection_id"]
            connection_name = connection["connection_name"]
            connection_type = connection["connection_type"]

            cols = st.columns(4)
            cols[0].markdown(
                f'#### <a href="http://localhost:8501/chat_sessions?user_id={user_id}&connection_id={connection_id}" target="_self">{connection_name}</a>',
                unsafe_allow_html=True,
            )
            if connection_type.lower() == "postgres":
                cols[1].markdown(f"##### :green[{connection_type}]")
            else:
                cols[1].markdown(f"##### :orange[{connection_type}]")
            if cols[2].button("📤", key=f"update_button_{connection_id}"):
                st.session_state.update_id = connection_id
            if (
                "update_id" in st.session_state
                and st.session_state.update_id == connection_id
            ):
                with st.form(key=f"update_form_{connection_id}"):
                    new_connection_name = st.text_input(
                        label="Connection Name", value=connection_name
                    )
                    new_connection_type = st.selectbox(
                        label="Connection Type",
                        options=["postgres", "mysql"],
                        index=0 if connection_type == "postgres" else 1,
                    )
                    new_db_host = st.text_input(
                        label="DB Host", value=connection["db_host"]
                    )
                    new_db_port = st.text_input(
                        label="DB Port", value=connection["db_port"]
                    )
                    new_db_name = st.text_input(
                        label="DB Name", value=connection["db_name"]
                    )
                    new_db_user = st.text_input(
                        label="DB User", value=connection["db_username"]
                    )

                    if st.form_submit_button(label="Save Changes"):
                        payload = {
                            "connection_name": new_connection_name,
                            "connection_type": new_connection_type,
                            "db_host": new_db_host,
                            "db_port": new_db_port,
                            "db_name": new_db_name,
                            "db_username": new_db_user,
                        }
                        update_connection(connection_id, payload)

                # add a close button to close the form
                if st.button(label="Close"):
                    del st.session_state.update_id

            if cols[3].button(
                "❌", key=f"delete_button_{connection_id}", type="secondary"
            ):
                st.write(f"Deleting connection {connection_id}")
                if delete_connection(connection_id):
                    st.experimental_rerun()

            st.write("---")
    else:
        st.write("You don't have any connections yet.")
