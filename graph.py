from langgraph.graph import StateGraph, END
from agent.nodes import (
    extract_intent_node,
    generate_sql_node,
    validate_sql_node,
    execute_sql_node,
    generate_response_node,
)
from typing import Dict

from typing import TypedDict, List, Dict

class AgentState(TypedDict):
    query: str
    schema: str
    intent: str
    sql: str
    result: Dict
    summary: str
    error: str


def build_agent_graph():
    """Builds the full Text-to-SQL LangGraph pipeline."""

    # Create graph with state schema
    graph = StateGraph(name="Text-to-SQL Agent", state_schema=AgentState)

    # Add nodes
    graph.add_node("extract_intent", extract_intent_node)
    graph.add_node("generate_sql", generate_sql_node)
    graph.add_node("validate_sql", validate_sql_node)
    graph.add_node("execute_sql", execute_sql_node)
    graph.add_node("generate_response", generate_response_node)

    # Define flow
    graph.set_entry_point("extract_intent")
    graph.add_edge("extract_intent", "generate_sql")
    graph.add_edge("generate_sql", "validate_sql")
    graph.add_edge("validate_sql", "execute_sql")
    graph.add_edge("execute_sql", "generate_response")
    graph.add_edge("generate_response", END)

    return graph.compile()
