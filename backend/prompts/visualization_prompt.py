import json


def build_visualization_prompt(question: str, dataframe) -> str:
    """
    Build prompt for the Visualization Agent.

    Parameters:
        question: User's natural language question.
        dataframe: SQL result as a Pandas DataFrame.
    """

    columns = dataframe.columns.tolist()

    sample_data = dataframe.head(10).to_dict(orient="records")

    return f"""
You are an expert Data Visualization Assistant.

Your job is to analyze the user's question and the SQL query result, then decide the most appropriate visualization.

User Question:
{question}

Columns:
{columns}

Sample Data:
{json.dumps(sample_data, indent=2)}

Choose ONLY ONE chart from the following:

- bar
- line
- pie
- histogram
- scatter
- table

Guidelines:

1. Use "line" only when data represents time or trends.
2. Use "bar" for comparing categories.
3. Use "pie" for proportions or percentages.
4. Use "histogram" for showing the distribution of a single numeric column.
5. Use "scatter" when comparing two numeric variables.
6. Use "table" if a chart is not meaningful.

Return ONLY valid JSON.

Example:

{{
    "chart_type": "bar",
    "x_column": "category",
    "y_column": "revenue",
    "title": "Revenue by Category"
}}

Rules:
- Do not explain your reasoning.
- Do not return markdown.
- Do not wrap JSON inside ``` blocks.
- Return ONLY the JSON object.
"""