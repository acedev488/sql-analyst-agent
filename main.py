import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from rich.console import Console
from rich.panel import Panel

from agent.graph import build_graph
from agent.tools import get_schema
from data.seed_db import DB_PATH, build_database

console = Console()


def get_connection() -> sqlite3.Connection:
    if not Path(DB_PATH).exists():
        console.print(f'[dim]No database found, generating sample data at {DB_PATH}...[/dim]')
        build_database()
    return sqlite3.connect(DB_PATH)


def main():
    load_dotenv()
    if not os.getenv('OPENAI_API_KEY'):
        console.print('[red]Set OPENAI_API_KEY in your environment or .env file first.[/red]')
        return

    conn = get_connection()
    schema = get_schema(conn)
    llm = ChatOpenAI(model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'), temperature=0)
    app = build_graph(conn, llm)

    console.print(Panel.fit(schema, title="Database schema"))
    console.print("Ask a question about the data (or type 'exit'):\n")

    while True:
        question = console.input("[bold cyan]> [/bold cyan]")
        if question.strip().lower() in ('exit', 'quit'):
            break

        state = {'question': question, 'schema': schema, 'max_attempts': 3, 'attempts': 0}
        result = app.invoke(state)

        console.print(Panel(result["sql"], title="Generated SQL", style="yellow"))
        if result.get("chart_path"):
            console.print(f"[green]Chart saved to {result['chart_path']}[/green]")
        console.print(Panel(result["final_answer"], title="Answer", style="green"))
        console.print()


if __name__ == "__main__":
    main()
