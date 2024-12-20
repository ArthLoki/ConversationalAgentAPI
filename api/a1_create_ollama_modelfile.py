import os
import subprocess
import time
from configs import model_path, modelfile_path, root_path
from abort_process import aborting_process

dirname = "modelfiles"
if not os.path.exists(dirname):
    os.mkdir(dirname)

def get_template_text(system_content: str):
    tt1 = """{{ if .System }}{{ .System }}\n{{- end }}\n{{- if .Tools }}When you receive a tool call response, use the output to format an answer to the orginal user question."""
    tt2 = """\n{{- end }}<|eot_id|>\n{{- range $i, $_ := .Messages }}\n{{- $last := eq (len (slice $.Messages $i)) 1 }}\n{{- if eq .Role "user" }}<|start_header_id|>user<|end_header_id|>\n{{- if and $.Tools $last }}\n\nGiven the following functions, please respond with a JSON for a function call with its proper arguments that best answers the given prompt.\n\nRespond in the format {"name": function name, "parameters": dictionary of argument name and its value}. Do not use variables."""
    tt3 = '''\n\n{{ range $.Tools }}\n{{- . }}\n{{ end }}\n{{ .Content }}<|eot_id|>\n{{- else }}\n\n{{ .Content }}<|eot_id|>\n{{- end }}{{ if $last }}<|start_header_id|>assistant<|end_header_id|>\n\n{{ end }}\n{{- else if eq .Role "assistant" }}<|start_header_id|>assistant<|end_header_id|>\n{{- if .ToolCalls }}\n{{ range .ToolCalls }}\n{"name": {{ .Function.Name }}, "parameters": {{ .Function.Arguments }}}{{ end }}\n{{- else }}\n\n{{ .Content }}\n{{- end }}{{ if not $last }}<|eot_id|>{{ end }}\n{{- else if eq .Role "tool" }}<|start_header_id|>ipython<|end_header_id|>\n\n{{ .Content }}<|eot_id|>{{ if $last }}<|start_header_id|>assistant<|end_header_id|>\n\n{{ end }}\n{{- end }}\n{{- end }}'''
    return tt1 + system_content + tt2 + tt3

def load_ollama():
    try:
        subprocess.Popen(["ollama", "serve"])
        time.sleep(3) # Wait for a few seconds for Ollama to load!
        return True
    except Exception as err:
        print(f"Error while loading ollama: {err}")
        return False


def write_on_modelfile(ollama_modelname: str, modelname: str, modelfile_name: str, system_content: str):
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

            '''
        )
        arq.close()
        return True
    except Exception as err:
        print(f"Error while writing on modelfile: {err}")
        return False


def create_modelfile(ollama_modelname: str, modelfile_name: str, modelname: str, system_content: str):

    try:
        resWriting = write_on_modelfile(ollama_modelname, modelname, modelfile_name, system_content)
        if not resWriting:
            if os.path.exists(os.path.join(modelfile_path, modelfile_name)):
                subprocess.Popen(["rm", os.path.join(modelfile_path, modelfile_name)])
                print(f"\nDeleting modelfile {modelfile_name} created...")
            aborting_process()

        return True
    except Exception as err:
        print(f"Error while creating modelfile: {err}")
        return False
