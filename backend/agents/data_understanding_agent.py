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
            "business_type": business_summary["business_type"],
            "business_summary": business_summary
            
        }


