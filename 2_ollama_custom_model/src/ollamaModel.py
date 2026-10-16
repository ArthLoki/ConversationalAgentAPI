import os
import subprocess
from src.configs import modelfile_path
from src.modelfile import load_ollama, create_modelfile
from src.abort_process import aborting_process


def checkModelfile(modelfile_name: str):
    # if not modelfile_name.endswith(".modelfile"):
    #     modelfile_name = f"{modelfile_name}.modelfile"

    full_path = os.path.join(modelfile_path, modelfile_name)
    return os.path.exists(full_path)


def create_ollama_model(
    model_image: str, modelname: str, modelfile_name: str, system_content: str
):
    try:
        load_ollama()
        modelfileAlreadyExists = checkModelfile(modelfile_name)
        if not modelfileAlreadyExists:
            resCreateModelfile = create_modelfile(
                modelname, modelfile_name, system_content
            )
            if not resCreateModelfile:
                aborting_process()
                exit(1)

        subprocess.Popen(
            [
                "ollama",
                "create",
                model_image,
                "-f",
                os.path.join(modelfile_path, modelfile_name),
            ]
        )
        return True
    except Exception as err:
        print(f"Error while creating ollama model: {err}")
        return False
