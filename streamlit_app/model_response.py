import datetime
from urllib.parse import quote_plus

from dotenv import load_dotenv
from llama_index import GPTSQLStructStoreIndex, SQLDatabase
from sqlalchemy import create_engine, inspect

# from langchain import OpenAI
# from llama_index import LLMPredictor


load_dotenv()


# move everything to a class
class ModelResponse:
    def __init__(
        self, connection_type, db_host, db_port, db_name, db_username, db_password
    ):
        db_password = quote_plus(db_password)

        if connection_type == "postgres":
            connection = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
        elif connection_type == "mysql":
            connection = f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
        self._engine = create_engine(connection)

    def get_table_names(self):
        table_names = inspect(self._engine).get_table_names()
        table_names = [name.replace("_", " ").title() for name in table_names]
        return table_names

    def create_index(self, table_name):
        table_name = table_name.replace(" ", "_").lower()
        sql_database = SQLDatabase(self._engine, include_tables=[table_name])

        # TODO: Play around with more models
        # changing predictor from `text-davinci-003` to `text-embedding-ada-002`
        # llm_predictor = LLMPredictor(
        #     llm=OpenAI(temperature=0, model_name="text-embedding-ada-002")
        # )
        # pprint(sql_database.metadata_obj.tables[f"analytics.{table_name}"])
        self.index = GPTSQLStructStoreIndex(
            [],
            # llm_predictor=llm_predictor,
            sql_database=sql_database,
            table_name=f"{table_name}",
        )

        # you can optionally save the index to disk & can load it later
        # self.index.save_to_disk("index.json")

    def generate_response(self, user_input):
        query_response = self.index.query(user_input, mode="default")
        sql_query = query_response.extra_info["sql_query"]
        print("\n\n\n")
        print("[INFO] User Input: ", user_input)
        print("[INFO] SQL Query: ", sql_query)
        # TODO: Need to format this properly
        list_reponse = [str(tup[0]) for tup in eval(query_response.response)]
        final_response = ", ".join(list_reponse)
        print("[INFO] Model Response: ", final_response)
        print("\n")
        return final_response
