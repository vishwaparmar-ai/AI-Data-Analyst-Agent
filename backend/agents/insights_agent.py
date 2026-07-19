from backend.services.data_processing import DatasetAnalyzer
from backend.services.insight_service import InsightService
from backend.services.LLM_service import LLMService
from backend.utils.logger import logger


class InsightAgent:

    def __init__(self):

        self.analyzer = DatasetAnalyzer()
        self.insight_service = InsightService()
        self.llm = LLMService()

    def run(
        self,
        file_path: str,
        dataset_type: str,
        business_summary: str
    ) -> dict:
        """
        Generate business insights for the cleaned dataset.
        """

        logger.info("=" * 60)
        logger.info("INSIGHT AGENT STARTED")
        logger.info("=" * 60)

        # -------------------------------------------------
        # Read cleaned dataset
        # -------------------------------------------------

        logger.info("Reading cleaned dataset...")

        df = self.analyzer.read_dataset(file_path)

        # -------------------------------------------------
        # Generate dataset profile
        # -------------------------------------------------

        logger.info("Generating dataset profile...")

        dataset_profile = self.insight_service.generate_profile(df)

        # -------------------------------------------------
        # Generate insights using Gemini
        # -------------------------------------------------

        logger.info("Generating business insights...")

        insights = self.llm.generate_insights(
            dataset_type=dataset_type,
            business_summary=business_summary,
            dataset_profile=dataset_profile
        )

        logger.info("Insight generation completed.")

        return {
            "dataset_type": dataset_type,
            "business_summary": business_summary,
            "dataset_profile": dataset_profile,
            "executive_summary": insights.get(
                "executive_summary",
                ""
            ),
            "insights": insights.get(
                "insights",
                []
            ),
            "recommendations": insights.get(
                "recommendations",
                []
            )
        }


