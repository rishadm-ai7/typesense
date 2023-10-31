import json
import typesense

client = typesense.Client({
  'nodes': [{
    'host': 'localhost',
    'port': '8108',
    'protocol': 'http'
  }],
  'api_key': 'xyz',
  'connection_timeout_seconds': 2000000
})

# Load data from the JSON file
with open('opzhive_task_data.json') as f:
    data = json.load(f)

task_schema = {
  'name': 'opzhive_data',
  'fields': [
    {'name': 'task_id', 'type': 'int32' },
    {'name': 'task_title', 'type': 'string' },
    {'name': 'task_description', 'type': 'string' },
    {'name': 'task_due_date', 'type': 'string' },
    {'name': 'task_owner_user_id', 'type': 'int32' },
    {'name': 'project_id', 'type': 'int32' },
    {'name': 'task_category_id', 'type': 'int32' },
    {'name': 'internal_publishable', 'type': 'bool' },
    {'name': 'global_pool_publishable', 'type': 'bool' },
    {'name': 'task_skills', 'type': 'string[]' },
    {'name': 'task_complexity', 'type': 'string' },
    {'name': 'task_priority', 'type': 'string' },
    {'name': 'task_effort', 'type': 'float' },
    {'name': 'task_tags', 'type': 'string[]' },
    {'name': 'is_deleted', 'type': 'bool' },
    {'name': 'task_type', 'type': 'string' },
    {'name': "task_icon_url", "type": "string"},
    {"name": "initial_published", "type": "bool"},
    {"name": "is_locked", "type": "bool"},
    {"name": "reviewer_id", "type": "int32"},
    {
            "name": "embedding",
            "type": "float[]",
            "embed": {
              "from": [
                "task_description"
              ],
              "model_config": {
                "model_name": "ts/all-MiniLM-L12-v2"
              }
            }
          }
  ]
}

#delete if needed
for item in client.collections.retrieve():
    if item.get('name') == "opzhive_data":
        print("Found myitem!")
        client.collections['opzhive_data'].delete()

# Create the schema
client.collections.create(task_schema)

# Iterate over the data and push it
for document in data:
    response = client.collections['opzhive_data'].documents.create(document)

search_parameters = {
          "q": "improve organisation",
          "query_by": "task_description,task_title",
          "collection": "opzhive_data",
          "prefix": "false"
        }

result = client.collections['opzhive_data'].documents.search(search_parameters)
hits = result["hits"]
result = []
for item in hits:
    document = item['document']
    document.pop("embedding", None)
    result.append(document)

# Now, the 'result' list contains the desired columns for each document
print(json.dumps(result))
