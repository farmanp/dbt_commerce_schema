import mermaid_to_json
import schema_to_tables
import json_to_schema
import time
import logging

logging.basicConfig(level=logging.INFO)

ERD_FILE_PATH = "erd.md"
JSON_DEFINITION = "model_definition.json"
COMMERCE_SCHEMA_YAML = 'commerce_schema.yml'
SQL_TABLES = "create_tables.sql"


if __name__ == "__main__":
    logging.info("Starting the conversion process...")
    time.sleep(1)
    logging.info("Step 1: Converting Mermaid diagram to JSON...")
    mermaid_to_json.execute(ERD_FILE_PATH, JSON_DEFINITION)
    logging.info("Step 1 Complete: JSON file generated at location: %s", JSON_DEFINITION)
    
    time.sleep(1)
    logging.info("Step 2: Converting JSON file to YAML...")
    json_to_schema.convert_json_to_yaml(JSON_DEFINITION, COMMERCE_SCHEMA_YAML)
    logging.info("Step 2 Complete: YAML file generated at location: %s", COMMERCE_SCHEMA_YAML)
    
    time.sleep(1)
    logging.info("Step 3: Generating SQL tables from YAML file...")
    schema_to_tables.generate_sql_model(COMMERCE_SCHEMA_YAML, SQL_TABLES)
    logging.info("Step 3 Complete: SQL tables generated at location: %s", SQL_TABLES)

    logging.info("Conversion process completed successfully. All files have been generated.")