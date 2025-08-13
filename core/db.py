import requests

def execute_sql(sql: str) -> dict:
    response = requests.post("http://localhost:8765/", data=sql.encode('utf-8'))
    response.raise_for_status()
    return response.json()
