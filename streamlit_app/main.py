import os
import webbrowser

import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def landing_page():
    # Setting the title and favicon
    st.set_page_config(
        page_title="Chat DB",
        page_icon=":speech_balloon:",
        initial_sidebar_state="collapsed",
    )

    # Adding the title and subheading
    st.write(
        """
    # Chat DB
    ## *Query your database the way you talk*
    """
    )

    # Adding a description section
    st.write(
        """
    ### :orange[What is Chat DB?]
    Chat DB is a revolutionary new way of querying your databases using natural language. With Chat DB, you can easily communicate with your database by simply typing out your queries in the same way you would talk to a human. No more struggling with complicated SQL syntax - with Chat DB, you can get the information you need in seconds.
    """
    )

    # Adding a button to the sign-up page
    st.write(
        """
    ### :orange[Try Chat DB today!]
    Ready to experience the power of natural language database querying? Sign up for Chat DB today and start exploring your data in a whole new way.
    """
    )
    signup_button()

    st.write(
        """
    ### :orange[How does it work?]
    Chat DB is incredibly easy to use. Simply sign up and connect your Postgres or MySQL database, and you're ready to start querying. Once you're connected, you can create multiple chat sessions, each one displaying a list of tables against which you can query and converse. You can even save your sessions, so you can pick up right where you left off.
        """
    )

    # Adding a demo video section
    st.write(
        """
    ### :orange[See Chat DB in action]
    Watch this short video to see how Chat DB works.
    """
    )

    # Adding a video placeholder
    video_file = open("demo.mp4", "rb")
    video_bytes = video_file.read()
    st.video(video_bytes)

    st.write(
        """
        ### :orange[Benefits of Chat DB]
        With Chat DB, you can save time and effort by using natural language to communicate with your database. Say goodbye to the frustration of trying to remember complicated SQL syntax or spending hours writing out complex queries. Chat DB makes it easy to get the information you need quickly and easily.
        """
    )


def signup_button():
    button_text = "Sign up"
    button_bg_color = "#0077c2"
    button_text_color = "#ffffff"
    button_border_radius = "5px"
    button_padding = "10px 20px"

    button_style = f"""
        <style>
            .stButton button {{
                background-color: {button_bg_color};
                color: {button_text_color};
                border-radius: {button_border_radius};
                padding: {button_padding};
                font-size: 16px;
                font-weight: bold;
                text-transform: uppercase;
                cursor: pointer;
                transition: all 0.3s ease-in-out;
            }}
            .stButton button:hover {{
                background-color: #0061a8;
            }}
        </style>
    """

    st.markdown(button_style, unsafe_allow_html=True)

    if st.button(button_text):
        url = f"{os.environ.get('APP_URL')}/signup"
        webbrowser.open(url)


if __name__ == "__main__":
    landing_page()
