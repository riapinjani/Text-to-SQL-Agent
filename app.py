# app.py
import streamlit as st
from agent.graph import build_agent_graph
import pandas as pd

st.set_page_config(page_title="Text-to-SQL Local Agent", layout="wide")

st.title("🧠 Text-to-SQL Local Agent")
st.markdown("Ask data questions in plain English. Runs locally with Ollama + LangGraph.")

with st.expander("⚙️ Database Metadata (Optional)"):
    schema_hint = st.text_area("Paste your database schema here", height=150)

user_query = st.text_input("Enter your data question:", placeholder="e.g., Show me total sales by region")

if st.button("Run Query") and user_query:
    with st.spinner("Generating SQL and fetching results..."):
        graph = build_agent_graph()
        inputs = {"query": user_query, "schema": schema_hint}
        outputs = graph.invoke(inputs)
        sql_query = outputs.get("sql", "")
        result = outputs.get("result", None)
        summary = outputs.get("summary", "")


    st.subheader("📝 Generated SQL")
    st.code(sql_query, language="sql")

    if isinstance(result, pd.DataFrame):
        st.subheader("📊 Query Results")
        st.dataframe(result)
        st.subheader("💬 Summary")
        st.write(summary)
    else:
        st.error(result)

    if isinstance(result, pd.DataFrame):
        st.subheader("📊 Query Results")
        st.dataframe(result)

        # Simple visualization if numeric columns exist
        numeric_cols = result.select_dtypes(include=["number"]).columns
        if len(numeric_cols) >= 1:
            st.subheader("📈 Quick Visualization")
            st.bar_chart(result[numeric_cols])
    else:
        st.error(result)
