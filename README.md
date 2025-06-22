# SQL Analyst Agent

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-agent-6f42c1)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

A small [LangGraph](https://github.com/langchain-ai/langgraph) agent that
answers natural-language questions about a database by writing and running
its own SQL. It retries automatically when a query fails, decides on its own
whether a chart would help, and produces a plain-English answer citing the
actual numbers.

## Why this exists

This is a case study in building a minimal, dependency-light agent loop
without hiding the mechanics behind a heavyweight framework: every node,
prompt, and routing decision lives in a small, readable file so the whole
control flow can be understood in one sitting.

## Architecture

```
                ┌──────────────────┐
   question --> │   generate_sql    │◄───────────────┐
                └────────┬──────────┘                │
                         │                            │ retry (error, attempts left)
                         ▼                            │
                ┌──────────────────┐                  │
                │    execute_sql    │──────────────────┘
                └────────┬──────────┘
             success │        │ give up (error, no attempts left)
                     ▼        ▼
         ┌────────────────────┐  ┌───────────┐
         │ decide_visualization│  │ summarize │◄── (both paths converge here)
         └──────────┬──────────┘  └─────┬─────┘
                    └─────────────────► │
                                        ▼
                                     answer
```

Each box in `agent/graph.py` is a plain Python function in `agent/nodes.py`
that reads and writes a shared `AgentState` (`agent/state.py`). Routing
decisions (retry vs. give up vs. proceed) are made by
`route_after_execute`, a single small function — no hidden framework magic.

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
(`data/sample.db`, built by `data/seed_db.py`) so there's something to query
out of the box. Ask questions like:

- "Which store had the highest revenue in November?"
- "Show me the daily revenue trend for the Downtown store in October."
- "What's our best-selling product by quantity?"

See [`examples/example_run.md`](examples/example_run.md) for a full sample
transcript, including a generated chart.

## Safety

The agent is restricted to read-only `SELECT` statements at both the prompt
level and the execution level (`agent/tools.py::run_sql`), so a
hallucinated `DROP TABLE` can't actually run.

## Tests

```bash
pytest
```

## Project layout

```
agent/
  state.py    # shared AgentState TypedDict
  prompts.py  # LLM prompt templates
  tools.py    # SQL execution, schema introspection, chart rendering
  nodes.py    # LangGraph node functions
  graph.py    # wires nodes into a StateGraph
data/
  seed_db.py  # synthetic dataset generator
main.py       # interactive CLI
tests/        # pytest unit tests
```
