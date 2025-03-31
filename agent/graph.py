import sqlite3

from langchain_core.language_models import BaseChatModel
from langgraph.graph import END, StateGraph

from agent.nodes import (
    make_decide_visualization_node,
    make_execute_sql_node,
    make_generate_sql_node,
    make_summarize_node,
    route_after_execute,
)
from agent.state import AgentState


def build_graph(conn: sqlite3.Connection, llm: BaseChatModel):
    graph = StateGraph(AgentState)

    graph.add_node('generate_sql', make_generate_sql_node(llm))
    graph.add_node('execute_sql', make_execute_sql_node(conn))
    graph.add_node('decide_visualization', make_decide_visualization_node(llm))
    graph.add_node('summarize', make_summarize_node(llm))

    graph.set_entry_point('generate_sql')
    graph.add_edge('generate_sql', 'execute_sql')
    # retry loops back into generate_sql; give_up skips straight to summarize
    graph.add_conditional_edges(
        'execute_sql',
        route_after_execute,
        {
            'retry': 'generate_sql',
            'give_up': 'summarize',
            'success': 'decide_visualization',
        },
    )
    graph.add_edge('decide_visualization', 'summarize')
    graph.add_edge('summarize', END)

    return graph.compile()
