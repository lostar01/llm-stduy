import chromadb
import requests

# Initialize the ChromaDB client
client = chromadb.Client()

# Connect to the existing collection
collection = client.get_collection("llama3_collection")  # Use your collection name

# Define the query text
query_text = "Tell me more about machine learning"

# Query ChromaDB for the most relevant documents based on the query
results = collection.query(
    query_texts=[query_text],
    n_results=3  # Get the top 3 most relevant results
)

# Extract relevant texts from the ChromaDB results
relevant_texts = [result['document'] for result in results['documents']]

# Concatenate the relevant texts to form the context
context = " ".join(relevant_texts)

# Define the API endpoint and headers for Ollama API
OLLAMA_API_URL = "http://127.0.0.1/v1/generate"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",  # Replace with your actual API key
    "Content-Type": "application/json"
}

# Prepare the payload for the Ollama LLaMA 3 API request
payload = {
    "model": "llama3",
    "prompt": context
}

# Make the API request to Ollama's LLaMA 3 model
response = requests.post(OLLAMA_API_URL, json=payload, headers=headers)

# Handle the response
if response.status_code == 200:
    generated_content = response.json().get('generated_text')
    print("Generated Response:", generated_content)
else:
    print("Failed to generate content:", response.status_code, response.text)

