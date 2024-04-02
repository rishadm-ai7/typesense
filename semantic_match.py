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

data = [
    {"product_name": "Cell phone"},
    {"product_name": "Laptop"},
    {"product_name": "Desktop"},
    {"product_name": "Printer"},
    {"product_name": "Keyboard"},
    {"product_name": "Monitor"},
    {"product_name": "Mouse"}
]

product_schema = {
  'name': 'products',
  'fields': [
    {'name': 'product_name', 'type': 'string' },
    {
            "name": "embedding",
            "type": "float[]",
            "embed": {
              "from": [
                "product_name"
              ],
              "model_config": {
                "model_name": "ts/all-MiniLM-L12-v2"
              }
            }
          }
  ]
}

#delete the collection if already exists
client.collections['products'].delete()

#create the schema
client.collections.create(product_schema)

#iterate over the data and push it
for document in data:
    response = client.collections['products'].documents.create(document)

search_parameters = {
          "q": "a device used to call",
          "query_by": "embedding",
          "collection": "products",
          "prefix": "false",
          "exclude_fields": "embedding",
          "per_page": 1
        }

result = client.collections['products'].documents.search(search_parameters)

result=json.dumps(result)
print(result)