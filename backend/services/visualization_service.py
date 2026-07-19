import plotly.express as px
import pandas as pd


class VisualizationService:
    """
    Generates Plotly visualizations from the chart plan
    returned by the LLM.
    """

    def generate_chart(self, df: pd.DataFrame, plan: dict):

        chart_type = plan.get("chart_type")
        title = plan.get("title", "Visualization")

        if chart_type == "bar":
            return self.create_bar_chart(df, plan, title)

        elif chart_type == "line":
            return self.create_line_chart(df, plan, title)

        elif chart_type == "pie":
            return self.create_pie_chart(df, plan, title)

        elif chart_type == "histogram":
            return self.create_histogram(df, plan, title)

        elif chart_type == "scatter":
            return self.create_scatter_chart(df, plan, title)

        elif chart_type == "table":
            return None

        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")



    def create_bar_chart(
        self,
        df: pd.DataFrame,
        plan: dict,
        title: str
    ):

        return px.bar(
            df,
            x=plan["x_column"],
            y=plan["y_column"],
            title=title,
            text_auto=True
        )

 

    def create_line_chart(
        self,
        df: pd.DataFrame,
        plan: dict,
        title: str
    ):

        return px.line(
            df,
            x=plan["x_column"],
            y=plan["y_column"],
            title=title,
            markers=True
        )


    def create_pie_chart(
        self,
        df: pd.DataFrame,
        plan: dict,
        title: str
    ):

        return px.pie(
            df,
            names=plan["x_column"],
            values=plan["y_column"],
            title=title
        )

  

    def create_histogram(
        self,
        df: pd.DataFrame,
        plan: dict,
        title: str
    ):

        return px.histogram(
            df,
            x=plan["x_column"],
            title=title
        )


    def create_scatter_chart(
        self,
        df: pd.DataFrame,
        plan: dict,
        title: str
    ):

        return px.scatter(
            df,
            x=plan["x_column"],
            y=plan["y_column"],
            title=title
        )

  

    def save_chart(
        self,
        fig,
        output_path: str
    ):
        """
        Save Plotly chart as JPG.
        """

        fig.write_image(
            output_path,
            format="jpg",
            scale=2
        )

        return output_path