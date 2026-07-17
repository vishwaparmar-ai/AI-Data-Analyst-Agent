def build_cleaning_prompt(report: dict) -> str:
    return f"""
You are an expert Data Cleaning Agent.

Analyze the dataset report below and decide the best cleaning strategy.

Dataset Report:
{report}

Rules:
1. Remove duplicate rows if duplicates exist.
2. Fill missing numeric values using mean, median, or zero (choose the best).
3. Fill missing categorical values using mode.
4. Convert detected date columns to datetime.
5. Remove invalid rows only if necessary.
6.If there are no missing numeric values,
7.set fill_numeric_missing to null.
8.If there are no missing categorical values,
9.set fill_categorical_missing to null.

Do not suggest unnecessary cleaning steps.

Return ONLY valid JSON.

Do NOT include:
- explanations
- markdown
- ```json
- comments


Output format:

{{
    "remove_duplicates": true,
    "fill_numeric_missing": "median",
    "fill_categorical_missing": "mode",
    "convert_date_columns": true,
    "remove_invalid_rows": false,
    "reason": "Median is robust for numeric columns."
}}
"""