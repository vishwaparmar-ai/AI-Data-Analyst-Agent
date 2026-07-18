def business_understanding(report:dict) -> str:
    return f"""
You are a senior business analyst.

Given this dataset metadata:

Report:
{report}


Determine:

1. Rows and columns
2. Business domain
3. Dataset purpose
4. Important columns
5. Business metrics
6. Overall summary

Do NOT include:
- explanations
- markdown
- ```json
- comments

Return JSON only.

Output format:
{{
    "business_type": "",
    "dataset_purpose": "",
    "important_columns": "",
    "business_summary": ",
    
}}
"""