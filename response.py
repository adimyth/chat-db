import json
import os
from pprint import pprint

from dotenv import load_dotenv
from langchain import OpenAI
from llama_index import GPTSQLStructStoreIndex, LLMPredictor, SQLDatabase
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
            f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",
        )
        # self.index = None

    def get_table_names(self):
        table_names = self._engine.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        ).fetchall()
        # split by underscore & convert to title case
        table_names = [name[0].replace("_", " ").title() for name in table_names]
        return table_names

    def create_index(self, table_name):
        table_name = table_name.replace(" ", "_").lower()
        sql_database = SQLDatabase(self._engine, include_tables=[table_name])
        # changing predictor from `text-davinci-003` to `text-embedding-ada-002`
        llm_predictor = LLMPredictor(
            llm=OpenAI(temperature=0, model_name="text-embedding-ada-002")
        )
        # pprint(sql_database.metadata_obj.tables[f"analytics.{table_name}"])
        self.index = GPTSQLStructStoreIndex(
            [],
            # llm_predictor=llm_predictor,
            sql_database=sql_database,
            table_name=f"{table_name}",
        )

    def generate_response(self, user_input):
        query_response = self.index.query(user_input, mode="default")
        sql_query = query_response.extra_info["sql_query"]
        print("\n\n\n")
        print("[INFO] User Input: ", user_input)
        print("[INFO] SQL Query: ", sql_query)
        list_reponse = [str(tup[0]) for tup in eval(query_response.response)]
        final_response = ", ".join(list_reponse)
        print("[INFO] Model Response: ", final_response)
        print("\n")
        return final_response
