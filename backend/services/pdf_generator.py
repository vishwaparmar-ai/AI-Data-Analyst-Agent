import os
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Image
)

from backend.template.report_template import (
    build_title,
    build_dataset_overview,
    build_business_summary,
    build_insights,
    build_recommendations,
    build_footer
)


class PDFGenerator:

    def __init__(self):

        self.output_dir = "reports"

        os.makedirs(self.output_dir, exist_ok=True)

    def create_pdf(
        self,
        dataset: dict,
        business_summary: str,
        chart_paths: list,
        insights: list,
        recommendations: list,
        output_filename: str
    ) -> str:

        output_path = os.path.join(
            self.output_dir,
            output_filename
        )

        doc = SimpleDocTemplate(output_path)

        elements = []

        # Title
        elements.extend(
            build_title()
        )

        # Dataset Overview
        elements.extend(
            build_dataset_overview(dataset)
        )

        # Business Summary
        elements.extend(
            build_business_summary(business_summary)
        )

        # Charts
        if chart_paths:

            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import Paragraph, Spacer

            styles = getSampleStyleSheet()

            elements.append(
                Paragraph("<b>Visualizations</b>", styles["Heading2"])
            )

            elements.append(
                Spacer(1, 10)
            )

            for chart in chart_paths:

                if os.path.exists(chart):

                    img = Image(
                        chart,
                        width=6 * inch,
                        height=4 * inch
                    )

                    elements.append(img)

                    elements.append(
                        Spacer(1, 15)
                    )

        # Insights
        elements.extend(
            build_insights(insights)
        )

        # Recommendations
        elements.extend(
            build_recommendations(recommendations)
        )


        # Footer
        elements.extend(
            build_footer()
        )

        doc.build(elements)

        return output_path