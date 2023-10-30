import requests
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

client.collections['products'].delete()

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

##create the schema
client.collections.create(product_schema)

##upload the dataset
with open('products.json') as json_file:
    documents = json_file.read()
    client.collections['products'].documents.import_(documents.encode('utf-8'))

search_parameters = {
          "q": "device used to click",
          "query_by": "embedding",
          "collection": "products",
          "prefix": "false",
          "exclude_fields": "embedding",
          "per_page": 1
        }

result = client.collections['products'].documents.search(search_parameters)

result=json.dumps(result)
print(result)

