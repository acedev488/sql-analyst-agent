import sqlite3
from pathlib import Path

import pytest

from agent.tools import get_schema, run_sql
from data.seed_db import build_database


@pytest.fixture()
def conn(tmp_path: Path):
    db_path = tmp_path / 'test.db'
    build_database(path=db_path, seed=1)
    connection = sqlite3.connect(db_path)
    yield connection
    connection.close()


def test_build_database_creates_expected_tables(conn):
    tables = {
        row[0]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }
    assert {'stores', 'products', 'sales'} <= tables


def test_get_schema_lists_columns(conn):
    schema = get_schema(conn)
    assert 'stores(' in schema
    assert 'sales(' in schema


def test_run_sql_returns_dataframe_on_success(conn):
    df, error = run_sql(conn, 'SELECT COUNT(*) AS n FROM sales')
    assert error is None
    assert df is not None
    assert df['n'].iloc[0] > 0


def test_run_sql_returns_error_on_bad_syntax(conn):
    df, error = run_sql(conn, 'SELEKT * FROM sales')
    assert df is None
    assert error is not None


def test_run_sql_rejects_non_select_statements(conn):
    df, error = run_sql(conn, 'DELETE FROM sales')
    assert df is None
    assert error == 'Only SELECT statements are allowed.'
