import os
import textwrap
import subprocess
import time
from src.configs import model_path, modelfile_path
from src.abort_process import aborting_process


def load_ollama():
    try:
        subprocess.Popen(["ollama", "serve"])
        time.sleep(3)  # Wait for a few seconds for Ollama to load!
        return True
    except Exception as err:
        print(f"Error while loading ollama: {err}")
        return False


def write_on_modelfile(
    modelname: str, modelfile_name: str, system_content: str
):
    full_model_path = os.path.join(model_path, modelname)
    full_modelfile_path = os.path.join(modelfile_path, modelfile_name)

    # Usa textwrap.dedent para ignorar a indentação do código Python
    content = textwrap.dedent(f'''\
        FROM "{full_model_path}"

        # PARAMETERS
        PARAMETER temperature 0.52
        PARAMETER num_ctx 2048

        # STOP TOKENS (ChatML)
        PARAMETER stop "<|im_end|>"
        PARAMETER stop "<|im_start|>"

        # TEMPLATE (Com {{ .Response }})
        TEMPLATE """{{{{ if .System }}}}<|im_start|>system
        {{{{ .System }}}}<|im_end|>
        {{{{ end }}}}{{{{ if .Prompt }}}}<|im_start|>user
        {{{{ .Prompt }}}}<|im_end|>
        {{{{ end }}}}<|im_start|>assistant
        {{{{ .Response }}}}<|im_end|>"""

        # SYSTEM
        SYSTEM """{system_content}"""
    ''')

    try:
        with open(full_modelfile_path, "w", encoding="utf-8") as arq:
            arq.write(content)
        return True
    except Exception as err:
        print(f"Error while writing on modelfile: {err}")
        return False


def create_modelfile(modelname: str, modelfile_name: str, system_content: str):
    try:
        modelfile_name = f"{modelfile_name}.modelfile"
        resWriting = write_on_modelfile(modelname, modelfile_name, system_content)
        if not resWriting:
            if os.path.exists(os.path.join(modelfile_path, modelfile_name)):
                subprocess.Popen(["rm", os.path.join(modelfile_path, modelfile_name)])
                print(f"\nDeleting modelfile {modelfile_name} created...")
            aborting_process()

        return True
    except Exception as err:
        print(f"Error while creating modelfile: {err}")
        return False
