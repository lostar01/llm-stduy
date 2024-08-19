#!/usr/bin/python3

from FlagEmbedding import BGEM3FlagModel

# Function to generate embeddings
def vectorize_text(text):
    model = BGEM3FlagModel('BAAI/bge-m3',use_fp16=True)
    embedding = model.encode(text,
                            batch_size=12,
                            max_length=8192,
                            )['dense_vecs']
    return embedding

knowledge_slices = []

f = open("/tmp/test_content.txt","r")

while True:
   line = f.readline()
   if line:
       knowledge_slices.append(line)
   else:
       break

new_knowledge_slices = [knowledge_slices[i:i+50] for i in range(0,len(knowledge_slices),50)]

knowledge_vectors = [vectorize_text(slice) for slice in new_knowledge_slices]

# user query
query = "How many parameters does llama3 have ?"

query_vector = vectorize_text(query)

similarities = []
for t in knowledge_vectors:
    similarities.append(t @ query_vector.T)



#best_match_index = similarities.argmax()
#best_slice = new_knowledge_slices[best_match_index]
#

#print(f"Query: {query}")
#print(f"Most relevant knowledge slice: {best_slice}")
