import os
from pprint import pprint
from dotenv import load_dotenv
from llama_index import GPTSQLStructStoreIndex, SQLDatabase
from sqlalchemy import create_engine

load_dotenv()


# move everything to a class
class Response:
    def __init__(self):
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")

        self._engine = create_engine(
            f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        # self.index = None

    def get_table_names(self):
        table_names = self._engine.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'analytics'"
        ).fetchall()
        # split by underscore & convert to title case
        table_names = [name[0].replace("_", " ").title() for name in table_names]
        return table_names
    
    def create_index(self, table_name):
        table_name = table_name.replace(" ", "_").lower()
        sql_database = SQLDatabase(self._engine, schema="analytics", include_tables=[table_name])
        self.index = GPTSQLStructStoreIndex(
            [],
            sql_database=sql_database,
            table_name=f"{table_name}",
            schema="analytics",
        )

    def generate_response(self, user_input):
        response = self.index.query(user_input)
        return response
