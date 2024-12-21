import requests

url = "https://www.youtube.com/watch?v=xvCwZ73muV8&t=2065s"

resposta = requests.get(url)

print(resposta)