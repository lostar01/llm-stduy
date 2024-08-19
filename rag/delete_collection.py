import chromadb
client = chromadb.HttpClient(host='localhost', port=8000)
client.delete_collection('my_collection')

client.list_collections()
