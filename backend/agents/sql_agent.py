from backend.services.LLM_service import LLMService
from backend.services.sql_executor import SQLExecutor
from backend.utils.logger import logger


class SQLAgent:

    def __init__(self):
        self.llm = LLMService()
        self.executor = SQLExecutor()

    def run(self, file_path: str, question: str) -> dict:

        logger.info("Loading cleaned dataset...")

        df = self.executor.load_dataset(file_path)

        logger.info("Extracting dataset schema...")

        schema = self.executor.get_schema(df)

        logger.info("Generating SQL query using Gemini...")

        sql_query = self.llm.generate_sql(
            schema=schema,
            question=question
        )

        logger.info(f"Generated SQL:\n{sql_query}")

        logger.info("Executing SQL query...")

        result_df = self.executor.execute_query(
            df=df,
            sql_query=sql_query
        )

        logger.info("SQL query executed successfully.")

        result_json = result_df.to_dict(orient="records")

        logger.info("Generating natural language answer...")

        summary = self.llm.summarize_sql_result(
            question=question,
            results=result_json
        )

        return {
            "question": question,
            "answer": summary,
            "sql_query": sql_query,
            "result": result_json,
            "dataframe": result_df
        }


