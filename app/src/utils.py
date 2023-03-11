import os
from urllib.parse import quote_plus

from cryptography.fernet import Fernet
from dotenv import load_dotenv
from sqlalchemy import create_engine

from app.src.models.connection import Connection

load_dotenv()


def encrypt_password(password: str) -> str:
    key = os.getenv("SECRET_KEY")
    f = Fernet(key)
    token = f.encrypt(password.encode())
    return token.decode()


def check_valid_connection(connection: Connection):
    if connection.connection_type == "postgres":
        engine = create_engine(
            f"postgresql://{connection.db_username}:{quote_plus(connection.db_password)}@{connection.db_host}:{connection.db_port}/{connection.db_name}"
        )
    elif connection.connection_type == "mysql":
        engine = create_engine(
            f"mysql+mysqlconnector://{connection.db_username}:{quote_plus(connection.db_password)}@{connection.db_host}:{connection.db_port}/{connection.db_name}"
        )
    else:
        return False, "Invalid Connection Type"

    try:
        engine.connect()
        return True, None
    except Exception as e:
        msg = f"Invalid {connection.connection_type} connection: {e}"
        return False, msg
