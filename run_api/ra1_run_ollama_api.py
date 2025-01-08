import os
import requests
import json

def list_models():
    return {'1': "galybel", '2': "idris"}

def run_ollama_model(ollama_model, prompt):
    try:
        data = {
                "model": ollama_model, 
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
        }
        url = "http://localhost:11434/api/chat"

        response = requests.post(url, json=data)
        response_json = json.loads(response.text)

        ai_reply = response_json["message"]["content"]
        return ai_reply
    except Exception as e:
        print(f"\nError while running ollama api: {e}")
        return None
