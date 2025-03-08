import sqlite3

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from agent.prompts import SQL_RETRY_TEMPLATE, SQL_SYSTEM_PROMPT
from agent.state import AgentState
from agent.tools import run_sql


def make_generate_sql_node(llm: BaseChatModel):
    def generate_sql_node(state: AgentState) -> AgentState:
        if state.get('error'):
            user_prompt = SQL_RETRY_TEMPLATE.format(
                error=state['error'], sql=state['sql'], question=state['question']
            )
        else:
            user_prompt = state['question']

        response = llm.invoke([
            SystemMessage(content=SQL_SYSTEM_PROMPT.format(schema=state['schema'])),
            HumanMessage(content=user_prompt),
        ])
        sql = response.content.strip().strip('`').strip()
        if sql.lower().startswith('sql'):
            sql = sql[3:].strip()

        history = state.get('sql_history', [])
        return {
            'sql': sql,
            'sql_history': history + [sql],
            'attempts': state.get('attempts', 0) + 1,
        }

    return generate_sql_node


def make_execute_sql_node(conn: sqlite3.Connection):
    def execute_sql_node(state: AgentState) -> AgentState:
        df, error = run_sql(conn, state['sql'])
        return {'result_df': df, 'error': error}

    return execute_sql_node
