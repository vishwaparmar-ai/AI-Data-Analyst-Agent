import json


def build_sql_prompt(schema: dict, question: str) -> str:
    """
    Build a prompt for generating DuckDB SQL from a user's question.
    """

    return f"""
You are an expert SQL analyst.

Your task is to convert the user's question into a valid DuckDB SQL query.

Rules:
- Use ONLY the columns provided in the schema.
- Do NOT invent column names.
- The table name is dataset.
- Return ONLY the SQL query.
- Do NOT include explanations.
- Do NOT use markdown.
- The SQL must be executable in DuckDB.

Dataset Schema:
{json.dumps(schema, indent=4)}

User Question:
{question}

SQL:
"""