#!/usr/bin/python3

from FlagEmbedding import BGEM3FlagModel
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
import requests
import json

class MyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        # embed the documents somehow
        model = BGEM3FlagModel('BAAI/bge-m3',use_fp16=True)
        embeddings = model.encode(input,
                            batch_size=12,
                            max_length=8192,
                            )['dense_vecs']
        return embeddings.tolist()


emb_fn = MyEmbeddingFunction()

def vectorize_text(text):
    model = BGEM3FlagModel('BAAI/bge-m3',use_fp16=True)
    embeddings = model.encode(text,
                            batch_size=12,
                            max_length=8192,
                            )['dense_vecs']
    return embeddings.tolist()

# db connection
client = chromadb.HttpClient(host='localhost', port=8000)

collection = client.get_collection(name="my_collection", embedding_function=emb_fn)

# user query
query = "How many parameters does llama3 have ?"

query_vector = vectorize_text(query)


retrieved_documents = collection.query(
    query_embeddings=query_vector,
    n_results=2,
)

#for ts in result["metadatas"]:
#    for t in ts:
#        print(t["text"])
#        print("========================================================================")

prompt = f"""
Based on the provided context, give a fact-based answer to the following question:

Context:
{retrieved_documents}

User Query:
{query}

Answer:
"""


OLLAMA_API = "http://172.27.16.1:11434/api/generate"
data = {
    "model": "llama3",
    "prompt": prompt,
    "options": {
        "max_tokens": 150
    }
}


response = requests.post(OLLAMA_API, json=data)

res_list = response.text.split('\n')
for r in res_list:
    if r:
        j = json.loads(r)
    print(j.get("response"),end="")

print()

