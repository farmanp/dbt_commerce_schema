import json
import yaml  # This is actually PyYAML

def convert_json_to_yaml(json_file_path, yaml_file_path):
    # Load JSON data from file
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    # Check if the loaded JSON data is valid
    if not isinstance(json_data, dict) or 'entities' not in json_data:
        print("Invalid JSON data provided. It must be a dictionary with an 'entities' key.")
        return
    
    models = []
    for entity, fields in json_data['entities'].items():
        model = {
            'name': entity,
            'description': f"Table containing details for {entity}.",
            'columns': []
        }
        for field in fields:
            column = {
                'name': field['field_name'],
                'description': field['description'] or f"The {field['field_name']} of the {entity}."
            }
            # Adding tests based on data type and specific fields
            tests = []
            if field['type'] in ['varchar', 'datetime', 'boolean']:
                tests.append('not_null')
            if field['field_name'] == 'id' or field['field_name'].endswith('_id'):
                tests.append('unique')

            # Assume 'customer_id' relates to customers table for relational integrity checks
            if 'customer_id' in field['field_name']:
                tests.append({
                    'relationships': {
                        'to': 'ref("customers")',
                        'field': 'customer_id'
                    }
                })

            column['tests'] = tests
            model['columns'].append(column)
        models.append(model)

    yaml_output = {
        'version': 2,
        'models': models
    }

    # Write to YAML file
    with open(yaml_file_path, 'w') as yaml_file:
        yaml.dump(yaml_output, yaml_file, sort_keys=False, default_flow_style=False)

# Example usage:
# json_file_path = 'output/models.json'
# yaml_file_path = 'schema.yml'

# Converting to YAML
# convert_json_to_yaml(json_file_path, yaml_file_path)
