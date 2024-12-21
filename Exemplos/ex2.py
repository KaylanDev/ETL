import requests
import json
import os 
from dotenv import load_dotenv
load_dotenv()

api_key = os.environ.get("OPEN_API_KEY")

url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }


data = {
    "model" : "gpt-3.5-turbo-16k",
    "messages" : [{"role":"user","content":"ola tudo bem?"}]
}



resposta = requests.post(url,headers=headers,data=json.dumps(data))

print(resposta.json())