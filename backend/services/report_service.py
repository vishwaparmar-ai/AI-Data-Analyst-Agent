import os
import glob

from backend.services.pdf_generator import PDFGenerator


class ReportService:

    def __init__(self):
        self.pdf_generator = PDFGenerator()

    def generate_report(
        self,
        dataset,
        insights,
        recommendations,
        
    ):

        summary = dataset.business_summary

        dataset_info = {
            "file_name": dataset.file_name,
            "rows": dataset.total_rows,
            "columns": dataset.total_columns,
            "business_type": summary["business_type"]
        }

        chart_folder = f"charts/dataset_{dataset.id}"

        chart_paths = []

        if os.path.exists(chart_folder):

            chart_paths.extend(
                glob.glob(os.path.join(chart_folder, "*.png"))
            )

            chart_paths.extend(
                glob.glob(os.path.join(chart_folder, "*.jpg"))
            )

            chart_paths.extend(
                glob.glob(os.path.join(chart_folder, "*.jpeg"))
            )

        report_path = self.pdf_generator.create_pdf(
            dataset=dataset_info,
            business_summary=summary["business_summary"],
            chart_paths=chart_paths,
            insights=insights,
            recommendations=recommendations,
            output_filename=f"report_dataset_{dataset.id}.pdf"
        )

        return report_path