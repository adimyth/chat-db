import os
from urllib.parse import quote_plus

from cryptography.fernet import Fernet
from dotenv import load_dotenv
from mysql.connector import Error
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
        try:
            connection.db_password = quote_plus(connection.db_password)
            engine = create_engine(
                f"postgresql://{connection.db_username}:{connection.db_password}@{connection.db_host}:{connection.db_port}/{connection.db_name}"
            )
            engine.connect()
            return True
        except Exception as e:
            print(f"[ERROR] Invalid Postgres Connection: {e}")
            return False
    elif connection.connection_type == "mysql":
        try:
            connection.db_password = quote_plus(connection.db_password)
            engine = create_engine(
                f"mysql+pymysql://{connection.db_username}:{connection.db_password}@{connection.db_host}:{connection.db_port}/{connection.db_name}"
            )
            engine.connect()
            return True
        except Error as e:
            print(f"[ERROR] Invalid MySQL Connection: {e}")
            return False
