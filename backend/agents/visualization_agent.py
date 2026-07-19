import os
import pandas as pd

from backend.services.LLM_service import LLMService
from backend.services.visualization_service import VisualizationService
from backend.utils.logger import logger


CHART_DIR = "generated_charts"

os.makedirs(CHART_DIR, exist_ok=True)


class VisualizationAgent:

    def __init__(self):

        self.llm = LLMService()
        self.visualizer = VisualizationService()

    def run(
        self,
        question: str,
        dataframe: pd.DataFrame
    ) -> dict:

        logger.info("Generating visualization plan...")

        chart_plan = self.llm.generate_visualization_plan(
            question=question,
            dataframe=dataframe
        )

        logger.info(f"Chart Plan: {chart_plan}")

        figure = self.visualizer.generate_chart(
            dataframe,
            chart_plan
        )

        chart_path = None

        if figure is not None:

            filename = (
                chart_plan["title"]
                .replace(" ", "_")
                .lower()
            )

            chart_path = os.path.join(
            CHART_DIR,
            f"{filename}.jpg"
        )

            self.visualizer.save_chart(
                figure,
                chart_path
            )

            logger.info(f"Chart saved to {chart_path}")

        return {
            "chart_plan": chart_plan,
            "chart_path": chart_path
        }