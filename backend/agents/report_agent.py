from backend.services.report_service import ReportService
from backend.agents.insights_agent import InsightAgent


class ReportAgent:

    def __init__(self):
        self.insight_agent = InsightAgent()
        self.report_service = ReportService()

    def run(self, dataset):

        summary = dataset.business_summary

        result = self.insight_agent.run(
            file_path=dataset.cleaned_filepath,
            dataset_type=summary["business_type"],
            business_summary=summary["business_summary"]
        )

        report_path = self.report_service.generate_report(
            dataset=dataset,
            insights=result["insights"],
            recommendations=result["recommendations"],
        )

        return {
            "report_path": report_path
        }