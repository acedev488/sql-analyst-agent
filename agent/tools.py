import sqlite3
from typing import Optional, Tuple

import pandas as pd


def get_schema(conn: sqlite3.Connection) -> str:
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    )
    tables = [row[0] for row in cursor.fetchall()]

    lines = []
    for table in tables:
        cols = conn.execute(f"PRAGMA table_info({table})").fetchall()
        col_desc = ", ".join(f"{c[1]} {c[2]}" for c in cols)
        lines.append(f"- {table}({col_desc})")
    return "\n".join(lines)


def run_sql(conn: sqlite3.Connection, sql: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    stripped = sql.strip().rstrip(';')

    try:
        df = pd.read_sql_query(stripped, conn)
        return df, None
    except Exception as exc:
        return None, str(exc)
