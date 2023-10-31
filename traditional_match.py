import typesense
import json

#init client
client = typesense.Client({
  'nodes': [{
    'host': 'localhost',
    'port': '8108',
    'protocol': 'http'
  }],
  'api_key': 'xyz',
  'connection_timeout_seconds': 2
})

##define the schema
books_schema = {
  'name': 'books',
  'fields': [
    {'name': 'title', 'type': 'string' },
    {'name': 'authors', 'type': 'string[]', 'facet': True },

    {'name': 'publication_year', 'type': 'int32', 'facet': True },
    {'name': 'ratings_count', 'type': 'int32' },
    {'name': 'average_rating', 'type': 'float' }
  ],
  'default_sorting_field': 'ratings_count'
}

##create the schema
# client.collections.create(books_schema)

##list the collections 
collections = client.collections.retrieve()
print(collections)

##drop a collection
# client.collections['books'].delete()


##upload the dataset
with open('/tmp/books.jsonl') as jsonl_file:
  client.collections['books'].documents.import_(jsonl_file.read().encode('utf-8'))

search_parameters = {
  'q'         : 'Prejudeece',
  'query_by'  : 'title',
  'sort_by'   : 'average_rating:desc'
}

result = client.collections['books'].documents.search(search_parameters)

result=json.dumps(result)
print(result)
