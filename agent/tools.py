import sqlite3
from pathlib import Path
from typing import Optional, Tuple

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

CHARTS_DIR = Path(__file__).resolve().parent.parent / "charts"


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


def render_chart(df: pd.DataFrame, chart_type: str, title: str) -> Optional[str]:
    if chart_type not in {'bar', 'line'} or df.shape[1] < 2 or df.empty:
        return None

    CHARTS_DIR.mkdir(exist_ok=True)
    x_col, y_col = df.columns[0], df.columns[1]

    fig, ax = plt.subplots(figsize=(7, 4))
    if chart_type == 'bar':
        ax.bar(df[x_col].astype(str), df[y_col])
    else:
        ax.plot(df[x_col].astype(str), df[y_col], marker='o')

    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(title)
    plt.xticks(rotation=45, ha='right')
    fig.tight_layout()

    out_path = CHARTS_DIR / 'latest_chart.png'
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return str(out_path)
