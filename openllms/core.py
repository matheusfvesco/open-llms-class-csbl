import requests
import os
import json

def install_ollama_model(model_name: str):
    url = os.environ["OPENAI_BASE_URL"].replace("v1/","api/pull/")

    data = {
        "name": model_name,
        "stream": False
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(data), headers=headers)

    #print(response.text)
    #print(response.content)
    #print(response.url)

    return response.json().get("status") == "success"

def uninstall_ollama_model(model_name: str):
    url = os.environ["OPENAI_BASE_URL"].replace("v1/","api/delete/")
    data = {
        "name": model_name,
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.delete(url, data=json.dumps(data), headers=headers)

    #print(response)
    #print(response.text)
    #print(response.content)
    #print(response.url)

    if response.status_code == 200:
        return True
    return False
    