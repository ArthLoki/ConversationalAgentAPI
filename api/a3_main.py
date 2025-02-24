import os
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
        # os.system("""curl http://localhost:11434/api/chat -d '{ "model": {}, "messages": {} }'""".format(model_image, messages))

        # subprocess.Popen(["ollama", "run", model_image])
    except Exception as err:
        print(f"\nAn error ocurred while running new model: {err}")
        exit(1)

def main():
    print("\n>>> Step 1: Create a Modelfile by answering a few questions")
    modelfile_name = input("\nChoose a name for the modelfile: ")
    print("\n-----------------\nOLLAMA MODELS VALID MODELS:\n{}\n-----------------\n".format("\n".join(gguf_models)))
    modelname = input("\nEnter a valid model name: ")
    system_content = input("\nEnter a custom system content: ")

    print("\n\n>>> Step 2: Create an Ollama model")
    model_image = input("\nChoose a name for your ollama model: ")
    resOllamaModel = create_ollama_model(model_image, modelfile_name, modelname, system_content)
    if not resOllamaModel:
        print("\nAn error occured. Try again later.")
        exit(1)

    # print("\n\n>>> Step 3: Test the new model")
    # message_content = input("\nEnter a message content: ")
    # runNewModel(model_image, message_content)
    return 0


if __name__ == "__main__":
    main()
