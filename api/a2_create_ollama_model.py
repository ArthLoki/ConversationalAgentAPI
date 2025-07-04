import os
import subprocess
from configs import modelfile_path
from a1_create_ollama_modelfile import load_ollama, create_modelfile
from abort_process import aborting_process


def create_ollama_model(model_image: str, modelname: str, modelfile_name: str, system_content: str):
    try:
        load_ollama()
        resCreateModelfile = create_modelfile(modelname, modelfile_name, system_content)
        if not resCreateModelfile:
            aborting_process()
            exit(1)

        subprocess.Popen(["ollama", "create", model_image, "-f", os.path.join(modelfile_path, modelfile_name)])
        return True
    except Exception as err:
        print(f"Error while creating ollama model: {err}")
        return False
