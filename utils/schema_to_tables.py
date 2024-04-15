import yaml
import os

def generate_sql_model(schema_file, output_file):
    with open(schema_file, 'r') as file:
        schema = yaml.safe_load(file)

    with open(output_file, 'w') as sql_file:
        sql_file.write("CREATE DATABASE IF NOT EXISTS ecommerce;\n\n")
        for model in schema.get('models', []):
            model_name = model['name']
            columns = model['columns']
            sql_file.write(f"CREATE TABLE ecommerce.{model_name}\n")
            sql_file.write("(\n")
            for col in columns:
                # Assuming all columns are of type String for simplicity
                # You might want to modify this to suit your actual data types
                sql_file.write(f"    {col['name']} String,\n")
            sql_file.write(") ENGINE = MergeTree ORDER BY (")
            sql_file.write(", ".join([f"{col['name']}" for col in columns]))
            sql_file.write(");\n\n")