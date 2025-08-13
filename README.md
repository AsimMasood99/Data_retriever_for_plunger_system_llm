# Plunger Lift Data Retriever

This project is an AI-powered pipeline that answers natural language questions about a plunger lift system by dynamically generating and executing SQL queries.

## Project Structure

-   `main.py`: Main script that orchestrates the entire AI pipeline from user query to final answer.
-   `prompt_manifest.json`: The central control file. It registers all prompts, points to their template files, and defines their required variables.
-   `req.txt`: A list of all required Python packages. To install, run `pip install -r req.txt`.

### Directories

-   **`/prompts/`**: Contains all LLM prompt templates as `.md` files. This separation allows for easy editing of prompts without changing Python code.
-   **`/injections/`**: Stores large, static blocks of text (e.g., `injection.json`) that provide domain-specific context to the LLM during prompt formatting.
-   **`/promptManager/`**: (If used) Contains the Python module responsible for loading and managing prompts based on the manifest.



├── index.ipynb
├── injections
│   ├── helper.py
│   └── injection.json
├── main.py
├── promptManager
├── prompt_manifest.json
├── prompts
│   ├── decomposer.md
│   ├── final_analyst.md
│   └── sqlquery.md
├── README.md
└── req.txt



