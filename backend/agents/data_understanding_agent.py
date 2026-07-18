from backend.services.data_processing import DatasetAnalyzer
from backend.services.LLM_service import LLMService
from backend.utils.logger import logger


class DataUnderstandingAgent:

    def __init__(self):
        self.analyzer = DatasetAnalyzer()
        self.llm = LLMService()

    def run(self, file_path: str) -> dict:

        logger.info("Reading dataset...")

        df = self.analyzer.read_dataset(file_path)

        logger.info("Analyzing dataset...")

        report = self.analyzer.analyze_dataset(df)

        logger.info("Generating business understanding using Gemini...")

        business_summary = self.llm.generate_business_summary(report)

        logger.info("Business understanding generated successfully.")

        return {
            "report": report,
            "business_summary": business_summary
        }


if __name__ == "__main__":

    agent = DataUnderstandingAgent()

    result = agent.run("uploads/ecommerce_data.csv")

    logger.info("=" * 60)
    logger.info("DATASET REPORT")
    logger.info("=" * 60)
    logger.info(result["report"])

    logger.info("=" * 60)
    logger.info("BUSINESS SUMMARY")
    logger.info("=" * 60)
    logger.info(result["business_summary"])