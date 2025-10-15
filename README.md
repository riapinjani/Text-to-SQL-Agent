# Text-to-SQL Local Agent

A **fully local AI data exploration tool** for data analysts.  
Ask questions in plain English → get instant SQL queries and visual results.

Built with:  
- [LangGraph](https://github.com/langchain-ai/langgraph) for agent orchestration  
- [Ollama](https://ollama.ai) for local LLM inference  
- [Streamlit](https://streamlit.io) for interactive UI  
- [SQLite](https://www.sqlite.org/) for local data execution  

---

## 🚀 Demo Preview

> Screenshot coming soon

![Demo Screenshot](path/to/screenshot.png)  <!-- leave placeholder for your screenshot -->

---

## Setup Instructions
 

1️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

2️⃣ Install and run Ollama

Download from ollama.ai and start the server:
```bash
ollama run llama3
```
3️⃣ Launch the Streamlit app
```bash
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

🧩 Features

 Natural language interface: Ask questions about your data in plain English

Privacy-first: Runs fully offline via Ollama

Visual exploration: View SQL results as dataframes + charts

Schema-aware: Optionally provide DB schema for better SQL accuracy

Next Steps: Extensible: Add memory support