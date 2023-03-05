import os

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


def decrypt_password(token: str) -> str:
    key = os.getenv("SECRET_KEY")
    f = Fernet(key)
    password = f.decrypt(token.encode())
    return password.decode()


def check_valid_connection(connection: Connection):
    if connection.connection_type == "postgres":
        try:
            engine = create_engine(
                f"postgresql://{connection.db_username}:{connection.db_password}@{connection.db_host}:{connection.db_port}/{connection.db_name}"
            )
            engine.connect()
            return True
        except Exception as e:
            print(f"[ERROR] Invalid Connection: {e}")
            return False
    elif connection.connection_type == "mysql":
        try:
            engine = create_engine(
                f"mysql://{connection.db_username}:{connection.db_password}@{connection.db_host}:{connection.db_port}/{connection.db_name}"
            )
            engine.connect()
            return True
        except Exception as e:
            print(f"[ERROR] Invalid Connection: {e}")
            return False
