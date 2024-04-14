import mermaid_to_json
import schema_to_tables
import json_to_schema
import time

FILE_PATH = "../erd.md"

if __name__ == "__main__":
# Convert the Mermaid diagram to a JSON file
    time.sleep(1)
    print("Converting Mermaid diagram to JSON...")
    mermaid_to_json.execute(FILE_PATH)    
    print("JSON file generated.")
    # Convert the JSON file to a YAML file
    time.sleep(1)
    print("Converting JSON file to YAML...")
    json_to_schema.convert_json_to_yaml('dbt_def.json', 'schema_2.yml')
    print("YAML file generated.")
    time.sleep(1)
    # Generate SQL tables from the YAML file
    print("Generating SQL tables from YAML file...")
    schema_to_tables.generate_sql_model('schema_2.yml', 'create_tables2.sql')
    print("SQL tables generated.")

    print("Done.")
