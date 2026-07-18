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

        logger.info("Executing SQL query...")

        result_df = self.executor.execute_query(
            df=df,
            sql_query=sql_query
        )

        logger.info("SQL query executed successfully.")

        return {
            "question": question,
            "schema": schema,
            "sql_query": sql_query,
            "result": result_df.to_dict(orient="records")
        }


if __name__ == "__main__":

    agent = SQLAgent()

    result = agent.run(
        file_path="cleaned_datasets/cleaned_ecommerce_data.csv",
        question="Which payment method generated the highest revenue?"
    )

    logger.info("=" * 60)
    logger.info("QUESTION")
    logger.info(result["question"])

    logger.info("=" * 60)
    logger.info("GENERATED SQL")
    logger.info(result["sql_query"])

    logger.info("=" * 60)
    logger.info("RESULT")
    logger.info(result["result"])