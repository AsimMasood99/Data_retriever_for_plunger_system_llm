import os
import json
from core.prompt_manager import load_prompt, inject_variables
from core.db import execute_sql
from injections.Plunger_helper import raw_json, schema_details
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  

# Load prompt manifest
with open("prompt_manifest.json") as f:
    manifest = json.load(f)

# Initialize model
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0
)

def get_chat_completion(prompt, model) -> str:
    response = model.invoke(prompt)
    return response.content.strip()

def run_pipeline(user_query: str) -> str:
    # Step 1: Decomposer
    decomposer_prompt = load_prompt(manifest["query_decomposer"]["path"])
    decomposer_input = inject_variables(decomposer_prompt, {
        "user_query": user_query,
        "event_tree": raw_json,
        "schema_details": schema_details
    })
    decomposed_output = get_chat_completion(decomposer_input, llm)
    print("\n🔍 Decomposed Output:\n", decomposed_output)
    decomposed_json = json.loads(decomposed_output)

    # Step 2: SQL Query Generator
    sql_prompt = load_prompt(manifest["sql_query_generator"]["path"])
    sql_input = inject_variables(sql_prompt, {
        "decomposed_events": decomposed_json,
        "schema_details": schema_details
    })
    sql_output = get_chat_completion(sql_input, llm)
    print("\n🧾 Generated SQLs:\n", sql_output)
    sql_queries = json.loads(sql_output)

    # Step 3: Query Database
    sql_results = {}
    for name, sql in sql_queries.items():
        print(f"\n📡 Running SQL for: {name}")
        result = execute_sql(sql)
        print(f"✅ Result for {name}:", result)
        sql_results[name] = result

    # Step 4: Final Analyst
    analyst_prompt = load_prompt(manifest["final_analyst"]["path"])
    analyst_input = inject_variables(analyst_prompt, {
        "user_query": user_query,
        "decomposed_info": decomposed_json,
        "sql_results": sql_results,
        "event_tree": raw_json,
        "schema_details": schema_details
    })
    final_output = get_chat_completion(analyst_input, llm)
    print("\n📈 Final Recommendation:\n", final_output)

    return final_output
