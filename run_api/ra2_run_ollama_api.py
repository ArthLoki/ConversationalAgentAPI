import requests
import json
from ra3_create_elastic_index import get_previous_messages_from_index_data
from abort_process import aborting_process

def list_models():
    return {'1': {"model": "galybel", "character": "Galybel"}, '2': {"model": "idris", "character": "Idris Dawnlight"}}


def chose_model():
        try:
            models_available = list_models()

            print(f"\n=====================\n")
            for key, value in models_available.items():
                print(f"{key}: Model: {value.get('model')}\n\tCharacter: {value.get('character')}")
            print(f"\n=====================\n")

            model_key = input("Choose a model to run (only the numeric value): ")

            values = models_available.get(str(model_key))
            if values is None:
                print("\nThe selected model key doesn't exist.\n")
                aborting_process()

            model_name = values.get("model")
            character_name = values.get("character")

            return model_name, character_name
        except Exception as e:
            print(f"Error while choosing the model: {e}\n")
            exit(0)

def run_ollama_model(es, ollama_model, prompt, index_name):
    try:
        messages = get_previous_messages_from_index_data(es, index_name)
        messages.append({"role": "user", "content": prompt})
        data = {
                "model": ollama_model, 
                "messages": messages,
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
