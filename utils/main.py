import mermaid_to_json
import schema_to_tables
import json_to_schema
import time

ERD_FILE_PATH = "../erd.md"
JSON_DEFINITION = "model_definition.json"
COMMERCE_SCHEMA_YAML ='commerce_schema_.yml'
SQL_TABLES = "create_tables.sql"


if __name__ == "__main__":
    time.sleep(1)
    print("Converting Mermaid diagram to JSON...")
    mermaid_to_json.execute(ERD_FILE_PATH, JSON_DEFINITION)
    print("JSON file generated.")
    # Convert the JSON file to a YAML file
    time.sleep(1)
    print("Converting JSON file to YAML...")
    json_to_schema.convert_json_to_yaml(JSON_DEFINITION, COMMERCE_SCHEMA_YAML)
    print("YAML file generated.")
    time.sleep(1)
    # Generate SQL tables from the YAML file
    print("Generating SQL tables from YAML file...")
    schema_to_tables.generate_sql_model(COMMERCE_SCHEMA_YAML, SQL_TABLES)
    print("SQL tables generated.")

    print("Done.")
