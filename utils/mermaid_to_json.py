import re
import json

def parse_mermaid(mermaid_str):
    # Finding all entity blocks
    entities_raw = re.findall(r'(\w+)\s*\{([\s\S]*?)\}', mermaid_str)

    entities = {}
    relationships = []
    entity_started = False  # Flag to track if entity parsing has started

    # Parsing entities
    for entity, fields_str in entities_raw:
        fields = []
        for line in fields_str.strip().split('\n'):
            parts = line.strip().split()
            if len(parts) >= 2:
                field_type, field_name = parts[:2]
                description = ' '.join(parts[2:])
                fields.append({'field_name': field_name, 'type': field_type, 'description': description})
        entities[entity] = fields
        entity_started = True  # Set flag to True when first entity is encountered

    # Parsing relationships
    if entity_started:  # Only parse relationships if entity_started is True
        relationship_lines = re.findall(r'(\w+)\s+([\|\}\{]+)--([\|o\{\}]+)\s*(\w+)\s*:\s*"(\d+\.\.\d+|\d+)"', mermaid_str)
        for from_entity, from_card, to_card, to_entity, cardinality in relationship_lines:
            relationships.append({
                'from': from_entity,
                'from_card': from_card,
                'to_card': to_card,
                'to': to_entity,
                'cardinality': cardinality
            })

    return entities, relationships

def convert_to_json(entities, relationships):
  """
  Converts the given entities and relationships into a JSON schema.

  Args:
    entities (list): A list of entities.
    relationships (list): A list of relationships.

  Returns:
    str: A JSON string representing the schema.

  """
  schema = {'entities': entities, 'relationships': relationships}
  return json.dumps(schema, indent=4)


# entities, relationships = parse_mermaid(mermaid_data)
# json_output = convert_to_json(entities, relationships)

# with open('models.json', 'w') as f:
#     f.write(json_output)

def execute(file_name, output_file_name):
    """
    Executes the conversion of a Mermaid diagram file to JSON format.

    Args:
        file_name (str): The path to the Mermaid diagram file.
        output_file_name (str): The path to the output JSON file.

    Returns:
        None
    """
    data = open(file_name, 'r', encoding='utf-8').read()
    entities, relationships = parse_mermaid(data)
    json_output = convert_to_json(entities, relationships)
    with open(output_file_name, 'w', encoding='utf-8') as output_file:
        output_file.write(json_output)
