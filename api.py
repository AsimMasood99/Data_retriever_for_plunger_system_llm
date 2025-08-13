import os
import json
import sys

# Ensure local project directory is prioritized
sys.path.insert(0, os.path.abspath("injections"))

from Plunger_helper import raw_json
from langchain_groq import ChatGroq
from dotenv import load_dotenv, find_dotenv
from collections import defaultdict
import re
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests

load_dotenv(find_dotenv())  

# --- LLM Setup ---
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0
)



def safe_format(template, **kwargs):
    return template.format_map(defaultdict(lambda: "", kwargs))


def clean_markdown_json(text):
    # Remove triple backticks + optional language tag
    cleaned = re.sub(r"^```(?:json)?\n", "", text)
    cleaned = re.sub(r"\n```$", "", cleaned)
    return cleaned.strip()



def get_chat_completion(prompt, model) -> str:
    response = model.invoke(prompt)
    return response.content.strip()

def execute_sql(sql: str) -> dict:
    print("\n Sending SQL to server:")
    print(sql)
    
    response = requests.post("http://localhost:8765/", data=sql)
    print(" Raw Response:", response.status_code, response.text)
    response.raise_for_status()
    return response.json()

app = FastAPI()

# Allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in prod
    allow_methods=["POST"],
    allow_headers=["*"]
)

# Request model
class ChatRequest(BaseModel):
    user_query: str

@app.post("/chat")
def chat(req: ChatRequest):
    user_query = req.user_query
    event_context = raw_json["PromptInjection"]

    # Decompose query
    decomposer_prompt = f"""
    You are a task decomposer. Break down the user's natural language question into a structured query that highlights what the user wants to know, what metrics or filters are involved, and what kind of result is expected.
    ## User Query:
    {user_query}
    Return a structured breakdown only.
    """.strip()
    structured_query = get_chat_completion(decomposer_prompt, llm)

    # Generate SQL
    sql_prompt = f"""
You are an expert SQL generator. Given a structured query and schema context, return a valid SQL query for an SQLite database. Do not explain anything.

## Structured Query:
{structured_query}
## Schema and Event Hierarchy:
{event_context}
ONLY return the SQL query.

""".strip()
    print("\nSending SQL generation prompt to LLM...")
    sql = get_chat_completion(sql_prompt, llm).strip().strip("```sql").strip("```").strip()
    sql = sql.rstrip(";") + ";"

    print("\nSQL Generated:\n", sql)

    # Execute SQL
    try:
        result = execute_sql(sql)
    except Exception as e:
        return {"error": str(e)}

    # Generate summary
    summary_prompt = f"""
You are a data analyst. Based on the following SQL query, its result, and the user’s original question, generate a clear and concise explanation that helps a human understand the insight in plain English.

## User Query:
{user_query}
## SQL Query:
{sql}
## Query Result:
{result}
Write a friendly, human-readable summary.
""".strip()
    final_summary = get_chat_completion(summary_prompt, llm)

    return {
        "structured_query": structured_query,
        "sql": sql,
        "result": result,
        "summary": final_summary
    }



# Run: uvicorn api:app --reload

