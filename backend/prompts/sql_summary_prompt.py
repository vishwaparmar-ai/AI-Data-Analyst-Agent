def build_sql_summary_prompt(question: str, results: list) -> str:
    return f"""
You are an AI Data Analyst.

The user asked:

"{question}"

The SQL query has already been executed.

Query Results:

{results}

Write a short, professional answer based ONLY on the query results.

Rules:
- Do not mention SQL.
- Do not mention tables.
- Do not make up information.
- Keep the answer under 50 words.
"""