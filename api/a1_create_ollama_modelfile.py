import os
import subprocess
import time
from configs import model_path, modelfile_path
from abort_process import aborting_process


def load_ollama():
    try:
        subprocess.Popen(["ollama", "serve"])
        time.sleep(3) # Wait for a few seconds for Ollama to load!
        return True
    except Exception as err:
        print(f"Error while loading ollama: {err}")
        return False


def write_on_modelfile(modelname: str, modelfile_name: str, system_content: str):
    try:
        arq = open(os.path.join(modelfile_path, modelfile_name), "w")
        arq.write(
            f'''FROM "{os.path.join(model_path, modelname)}"\
            \n# sets the temperature to 1 [higher is more creative, lower is more coherent]\
            \nPARAMETER temperature 0.52\
            \n# sets the context window size to 4096, this controls how many tokens the LLM can use as context to generate the next token\
            \nPARAMETER num_ctx 2048 ''' + '''\

            \nTEMPLATE """{{ if .System }}<|im_start|>system\
            \n{{ .System }}<|im_end|>\
            \n{{ end }}{{ if .Prompt }}<|im_start|>user\
            \n{{ .Prompt }}<|im_end|>\
            \n{{ end }}<|im_start|>assistant\
            """

            \n# sets a custom system message to specify the behavior of the chat assistant\
            \nSYSTEM ''' + f'''"""{system_content}"""\

            \nPARAMETER stop "<|start_header_id|>"\
            \nPARAMETER stop "<|end_header_id|>"\
            \nPARAMETER stop "<|eot_id|>"\
            \nPARAMETER stop "<|im_end|>"\

            '''
        )
        arq.close()
        return True
    except Exception as err:
        print(f"Error while writing on modelfile: {err}")
        return False


def create_modelfile(modelname: str, modelfile_name: str, system_content: str):

    try:
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
