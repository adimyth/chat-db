import requests

from dotenv import load_dotenv
import streamlit as st


load_dotenv()


def get_connections(user_id):
    response = requests.get(f"http://localhost:8000/db-connection?user_id={user_id}")
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
        print(response.json())
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


def connections_app():
    st.title("Connections")
    modify_existing_connections()
    create_new_connection()


def modify_existing_connections():
    st.header("Existing Connections")
    # TODO: replace hardcoded user_id with actual user_id
    user_id = "2f93c956-32d3-44f7-b3c1-e14aae9e4fe5"
    connections = get_connections(user_id=user_id)
    if connections:
        for connection in connections:
            connection_id = connection["connection_id"]
            connection_name = connection["connection_name"]
            connection_type = connection["connection_type"]

            cols = st.columns(5)
            cols[0].markdown(f"##### :green[{connection_id}]")
            cols[1].markdown(f"##### :red[{connection_name}]")
            cols[2].markdown(f"##### :blue[{connection_type}]")
            if cols[3].button("Update", key=f"update_button_{connection_id}"):
                st.session_state.update_id = connection_id
            if (
                "update_id" in st.session_state
                and st.session_state.update_id == connection_id
            ):
                placeholder = st.empty()
                placeholder.markdown(f":orange[Updating connection {connection_name}]")
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
                        print(f"Payload: {payload}")
                        update_connection(connection_id, payload)

                        placeholder.empty()

            if cols[4].button("Delete", key=f"delete_button_{connection_id}"):
                st.write(f"Deleting connection {connection_id}")
                if delete_connection(connection_id):
                    st.experimental_rerun()
    else:
        st.write("You don't have any connections yet.")


def create_new_connection():
    st.header("Create Connection")
    with st.expander("Create a new connection"):
        with st.form(key="connection_form"):
            connection_name = st.text_input(label="Connection Name")
            connection_type = st.selectbox(
                label="Connection Type", options=["postgres", "mysql"]
            )
            db_host = st.text_input(label="DB Host")
            db_port = st.text_input(label="DB Port")
            db_name = st.text_input(label="DB Name")
            db_user = st.text_input(label="DB User")
            db_password = st.text_input(label="DB Password", type="password")
            user_id = st.text_input(label="User ID")

            if st.form_submit_button(label="Create Connection"):
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
