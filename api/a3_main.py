import json
import subprocess
from configs import gguf_models
from a2_create_ollama_model import create_ollama_model
from abort_process import aborting_process

def runNewModel(model_image: str, content: str):
    try:
        messages = [
            { "role": "user", "content": content }
        ]
        modelMessages = {"model": model_image, "messages": messages}
        subprocess.Popen(["curl", "http://localhost:11434/api/chat", "-d", f"'{modelMessages}'"])
    except Exception as err:
        print(f"\nAn error ocurred while running new model: {err}")
        exit(1)

def main():
    print("\n>>> Step 1: Create a Modelfile by answering a few questions")
    modelfile_name = input("\nChoose a name for the modelfile: ")
    print("\n-----------------\nOLLAMA MODELS VALID MODELS:\n{}\n-----------------\n".format("\n".join(gguf_models)))
    modelname = input("\nEnter a valid model name: ")

    jsonSystemContent = json.load(open("utils/system_contents.json"))
    all_characters_name = list(jsonSystemContent.keys())
    print(all_characters_name)
    print(f"\n=====================\n")
    for i, name in enumerate(all_characters_name):
        print(f"Character {i+1 if len(str(i)) <= 9 else f'0{i+1}'}: {name}")
    print(f"\n=====================\n")
    character_index = int(input("\nChoose a character to create a modelfile for (only the numeric value): "))

    system_content = all_characters_name[character_index-1]

    print("\n\n>>> Step 2: Create an Ollama model")
    model_image = input("\nChoose a name for your ollama model: ")
    resOllamaModel = create_ollama_model(model_image.lower(), modelname, modelfile_name, system_content)
    if not resOllamaModel:
        print("\nAn error occured. Try again later.")
    exit(1)

    # print("\n\n>>> Step 3: Test the new model")
    # message_content = input("\nEnter a message content: ")
    # runNewModel(model_image, message_content)
    return


if __name__ == "__main__":
    main()
