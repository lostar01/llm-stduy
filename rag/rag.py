#!/usr/bin/python3

from FlagEmbedding import BGEM3FlagModel
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings

class MyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        # embed the documents somehow
        model = BGEM3FlagModel('BAAI/bge-m3',use_fp16=True)
        embeddings = model.encode(input,
                            batch_size=12,
                            max_length=8192,
                            )['dense_vecs']
        return embeddings.tolist()


## Function to generate embeddings
#def emb_fn(text):
#    model = BGEM3FlagModel('BAAI/bge-m3',use_fp16=True)
#    embedding = model.encode(text,
#                            batch_size=12,
#                            max_length=8192,
#                            )['dense_vecs']
#    return embedding

emb_fn = MyEmbeddingFunction()

knowledge_slices = []
tmp_text = ""
count = 0

f = open("/tmp/test_content.txt","r")

while True:
   line = f.readline()
   if line:
       if count > 50:
           knowledge_slices.append(tmp_text)
           count = 0
           tmp_text = ""
       tmp_text += line
       count += 1
   else:
       break


#knowledge_vectors = [vectorize_text(slice) for slice in new_knowledge_slices]

documents = []
for i,slice in enumerate(knowledge_slices):
    documents.append({"id": str(i+1) , "text": str(slice)})


# db connection
client = chromadb.HttpClient(host='localhost', port=8000)

collection = client.create_collection(name="my_collection", embedding_function=emb_fn)

collection.add(
    ids=[doc['id'] for doc in documents],
    documents=[doc['text'] for doc in documents],
    metadatas=[{"text": doc['text']} for doc in documents]
)
