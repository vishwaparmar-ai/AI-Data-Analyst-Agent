import os

from backend.services.data_processing import DatasetAnalyzer
from backend.services.LLM_service import LLMService
from backend.services.cleaning_executor import CleaningExecutor
from backend.utils.logger import logger


PROCESSED_DIR = "cleaned_datasets"

os.makedirs(PROCESSED_DIR, exist_ok=True)


class DataCleaningAgent:

    def __init__(self):
        self.cleaner = DatasetAnalyzer()
        self.llm = LLMService()
        self.executor = CleaningExecutor()

    def run(self, file_path: str) -> dict:

        logger.info("Reading dataset...")
        df = self.cleaner.read_dataset(file_path)

        logger.info("Analyzing dataset...")
        report = self.cleaner.analyze_dataset(df)

        logger.info("Generating cleaning plan...")
        cleaning_plan = self.llm.generate_cleaning_plan(report)

        logger.info("Executing cleaning plan...")
        cleaned_df, cleaning_summary = self.executor.execute(
            df=df,
            report=report,
            plan=cleaning_plan
        )

        logger.info("Dataset cleaned successfully.")

        # Generate output filename
        filename = os.path.basename(file_path)

        output_path = os.path.join(
            PROCESSED_DIR,
            f"cleaned_{filename}"
        )

        logger.info(f"Saving cleaned dataset to {output_path}")

        self.executor.save_dataset(
            cleaned_df,
            output_path
        )

        logger.info("Cleaned dataset saved successfully.")

        return {
            "report": report,
            "cleaning_plan": cleaning_plan,
            "cleaned_dataset_path": output_path,
            "cleaned_summary": cleaning_summary
        }


if __name__ == "__main__":

    agent = DataCleaningAgent()

    result = agent.run("uploads/ecommerce_data.csv")

    logger.info("=" * 60)
    logger.info("DATASET REPORT")
    logger.info("=" * 60)
    logger.info(result["report"])

    logger.info("=" * 60)
    logger.info("CLEANING PLAN")
    logger.info("=" * 60)
    logger.info(result["cleaning_plan"])

    logger.info("=" * 60)
    logger.info("CLEANED DATASET")
    logger.info("=" * 60)
    logger.info(result["cleaned_dataset_path"])