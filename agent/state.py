from typing import List, Optional, TypedDict

import pandas as pd


class AgentState(TypedDict, total=False):
    question: str
    schema: str
    max_attempts: int

    sql: str
    sql_history: List[str]
    error: Optional[str]
    attempts: int

    result_df: Optional[pd.DataFrame]
    needs_chart: bool
    chart_path: Optional[str]
    final_answer: str
