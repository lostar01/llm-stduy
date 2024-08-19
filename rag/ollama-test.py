import requests
import json

OLLAMA_API = "http://172.27.16.1:11434/api/generate"
data = {
    "model": "llama3",
    "prompt": "awscli how to get ec2 detail ?",
    "options": {
        "max_tokens": 150
    }
}


#curl http://localhost:11434/api/generate -X POST -d '{
#  "model": "llama2",
#  "prompt": "Write an introduction about quantum computing.",
#  "options": {
#    "max_tokens": 100
#  }
#}'
#

response = requests.post(OLLAMA_API, json=data)

res_list = response.text.split('\n')
for r in res_list:
    if r:
        j = json.loads(r)
    print(j.get("response"),end="")

print()
