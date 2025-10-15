import subprocess
from utils.sql_executor import execute_sql_query

# ---- Ollama helper ----
def run_ollama(prompt: str, model: str = "llama3") -> str:
    """Run Ollama locally and return the output text."""
    result = subprocess.run(
        ["ollama", "run", model, prompt],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


# ---- Node 1: Intent Extraction ----
def extract_intent_node(state):
    query = state.get("query", "")
    prompt = f"""
You are an assistant that identifies the user's analytical intent.
Given the user's input, describe the intent (e.g., aggregation, filtering, comparison).
Respond briefly in one sentence.

User query: {query}
    """
    intent = run_ollama(prompt)
    return {"intent": intent, "query": query}


# ---- Node 2: SQL Generation ----
def generate_sql_node(state):
    query = state.get("query", "")
    schema = state.get("schema", "")

    prompt = f"""
    You are a SQL assistant. Convert the following natural language request into valid SQL.
    User request: {query}
    Database schema: {schema}

    Output ONLY the SQL query. Do not add any explanations or quotes.
    """
    sql_query = run_ollama(prompt)

    # Optional: extract SQL using simple heuristics
    if "SELECT" in sql_query.upper():
        start = sql_query.upper().index("SELECT")
        sql_query = sql_query[start:]
    else:
        sql_query = "SELECT 1;"  # fallback safe query

    return {"sql": sql_query}


# ---- Node 3: SQL Validation ----
def validate_sql_node(state):
    sql_query = state.get("sql", "")

    prompt = f"""
You are an SQL validator.
Review the following SQL for syntax errors or invalid references.
If errors exist, correct them. Output only the corrected SQL.

SQL: {sql_query}
    """
    validated_sql = run_ollama(prompt)
    return {"sql": validated_sql}


# ---- Node 4: SQL Execution ----
import sqlite3
from data.sample_data import DB_PATH

def execute_sql_node(state):
    sql_query = state.get("sql", "")
    if not sql_query.strip().upper().startswith("SELECT"):
        return {"error": "SQL not valid. Execution skipped."}

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute(sql_query)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        return {"result": {"columns": columns, "rows": rows}, "sql": sql_query}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()




# ---- Node 5: Response Generation ----
def generate_response_node(state):
    sql_query = state.get("sql", "")
    result = state.get("result", None)

    # Optional: summarize data structure using Ollama
    prompt = f"""
You are a data analyst. Summarize the query result in one or two sentences.
SQL: {sql_query}
Table shape: {getattr(result, 'shape', 'N/A')}
Columns: {getattr(result, 'columns', [])}

Generate a short summary for a business user.
    """
    summary = run_ollama(prompt)
    return {"summary": summary, "result": result, "sql": sql_query}
