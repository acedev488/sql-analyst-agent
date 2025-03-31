SQL_SYSTEM_PROMPT = """You are a senior data analyst who writes SQLite queries.

Rules:
- Use only the tables and columns provided in the schema below.
- Prefer explicit column names over `SELECT *`.
- Return ONLY the SQL query, with no markdown fences and no commentary.

Database schema:
{schema}
"""

SQL_RETRY_TEMPLATE = """The previous query failed with this error:

{error}

Previous query:
{sql}

Please write a corrected query that answers the original question:
{question}
"""

CHART_DECISION_PROMPT = """Given this question and the resulting data (shown as a
small preview), decide whether a chart would help communicate the answer.

Question: {question}

Data preview:
{preview}

Respond with exactly one word: "bar", "line", or "none".
- Use "bar" for comparisons across categories.
- Use "line" for trends over time.
- Use "none" if the result is a single value or a chart wouldn't add value.
"""

SUMMARY_PROMPT = """You are summarizing query results for a business user who
cannot read SQL.

Question: {question}

SQL used:
{sql}

Result data (preview):
{preview}

Write a concise (2-4 sentence) natural-language answer to the question, citing
concrete numbers from the data. Do not mention SQL or tables explicitly.
"""
