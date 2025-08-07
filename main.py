import json

manifest_path="prompt_manifest.json"


class PromptManager:
    """
    Manages loading and formatting prompts using a manifest file.
    This class is the core of the prompt orchestration system.
    """
    def __init__(self, manifest_path):
        self.manifest = self._load_manifest(manifest_path)
        self.loaded_prompts_cache = {}

    def _load_manifest(self, manifest_path):
        try:
            with open(manifest_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"FATAL ERROR: Could not load manifest file at {manifest_path}. Details: {e}")
            return None

    def _get_prompt_template(self, prompt_name):
        if prompt_name in self.loaded_prompts_cache:
            return self.loaded_prompts_cache[prompt_name]
        
        prompt_info = self.manifest.get(prompt_name, {})
        filepath = prompt_info.get('file')
        if not filepath:
            print(f"ERROR: No file path defined for prompt '{prompt_name}' in manifest.")
            return None
        
        try:
            with open(filepath, 'r') as f:
                template = f.read()
                self.loaded_prompts_cache[prompt_name] = template
                return template
        except FileNotFoundError:
            print(f"ERROR: Prompt file not found at {filepath}")
            return None

    def get_formatted_prompt(self, prompt_name, data):
        if not self.manifest or prompt_name not in self.manifest:
            print(f"ERROR: Prompt '{prompt_name}' not found in the manifest.")
            return None

        prompt_info = self.manifest[prompt_name]
        required_vars = set(prompt_info.get('variables', []))
        provided_vars = set(data.keys())

        if not required_vars.issubset(provided_vars):
            missing_vars = required_vars - provided_vars
            print(f"ERROR: Missing required variables for '{prompt_name}': {missing_vars}")
            return None

        template = self._get_prompt_template(prompt_name)
        if template is None:
            return None

        try:
            return template.format(**data)
        except KeyError as e:
            print(f"Formatting Error: Placeholder {e} is missing in the template.")
            return None

def load_injection_data(filepath='injections/injection.json'):
    """Loads the static context data from the injection file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"FATAL ERROR: Could not load injection data file at {filepath}. Details: {e}")
        return None

# --- Main Orchestration Logic ---
def main():
    print("--- Starting Plunger System Data Retriever ---")

    # 1. Initialize the PromptManager with our manifest
    prompt_manager = PromptManager('prompt_manifest.json')
    if not prompt_manager.manifest:
        return # Stop if manifest failed to load

    # 2. Load all static injection data (event details, etc.)
    injection_data = load_injection_data()
    if not injection_data:
        return # Stop if injection data failed to load

    # 3. Define the user's query and the database schema
    user_query = "Show me all plunger arrivals with unsafe velocity in the last 24 hours. Also, I need the average casing pressure for cycles with low flow yesterday."
    db_schema = "CREATE TABLE PLUNGER_UNSAFE_VELOCITY_EVENTS (...);\nCREATE TABLE UNEXPECTED_LOW_FLOW_EVENTS (...);\nCREATE TABLE BASIC_PRESSURE_EVENTS (...);"
    
    print(f"\n[Step 1] User Query Received: \"{user_query}\"")

    # 4. Use the PromptManager to format the first prompt (decomposer)
    decomposer_prompt_data = {"query": user_query}
    decomposer_prompt = prompt_manager.get_formatted_prompt('query_decomposer', decomposer_prompt_data)

    if not decomposer_prompt:
        print("Failed to generate the decomposer prompt. Exiting.")
        return

    print("\n[Step 2] Generated Decomposer Prompt for first LLM call.")
    # print(decomposer_prompt) # Uncomment to see the full prompt
    
    # 5. SIMULATE the first LLM call and its response
    # In a real application, you would send `decomposer_prompt` to an LLM API.
    print("\n[Step 3] Simulating LLM response (decomposed scenarios)...")
    simulated_llm_response_json = """
    {
      "description1": "Retrieve all plunger arrival events that had an unsafe velocity within the last 24 hours.",
      "description2": "Calculate the average casing pressure for all cycles that were flagged for low flow yesterday."
    }
    """
    scenarios = json.loads(simulated_llm_response_json)
    print("Scenarios received:", json.dumps(scenarios, indent=2))

    # 6. Loop through each scenario and generate a SQL query prompt
    print("\n[Step 4] Generating SQL Query Prompts for each scenario...")
    for key, description in scenarios.items():
        print(f"\n--- Processing {key}: \"{description}\" ---")
        
        # Prepare the data for the SQL generator prompt
        sql_generator_data = {
            "schema": db_schema,
            "event_details": injection_data.get("event_details", "Event details not found."),
            "description": description
        }
        
        # Use the PromptManager to format the second prompt
        sql_generator_prompt = prompt_manager.get_formatted_prompt('sql_query_generator', sql_generator_data)
        
        if sql_generator_prompt:
            print(f"Successfully generated SQL generator prompt for {key}.")
            # print(sql_generator_prompt) # Uncomment to see the full prompt for the second LLM
            # In a real app, you would now send this prompt to another LLM to get the final SQL query.
        else:
            print(f"Failed to generate SQL generator prompt for {key}.")

if __name__ == "__main__":
    main()