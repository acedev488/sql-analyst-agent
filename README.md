# SQL Analyst Agent

A LangGraph agent that answers natural-language questions about a database by
writing and running its own SQL, retrying on errors, and deciding when a chart
would help.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # add your OPENAI_API_KEY
```

## Usage

```bash
python main.py
```

The first run generates a small synthetic coffee-shop sales dataset
(`data/sample.db`) so there's something to query out of the box. Ask
questions like:

- "Which store had the highest revenue in November?"
- "Show me daily revenue trend for the Downtown store in October."
- "What's our best-selling product by quantity?"
