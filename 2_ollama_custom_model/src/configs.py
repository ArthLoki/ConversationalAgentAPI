import os, json


# Lambda Functions
joinPath = lambda directory: "/".join(directory)
customSystemContent = lambda description: {"role": "system", "content": description}  # for messages (chatbot history messages)


# Get Path Variables
current_path = os.getcwd()
root_path = (
    joinPath(os.getcwd().split("/")[:-1]) 
    if os.getcwd().split("/")[-1] != "ConversationalAgentAPI" 
    else os.getcwd() # ".../ConversationalAgentAPI"
)
current_directory = os.path.dirname(current_path)


# Set path variables
static_path = f"{root_path}/1_finetuning/static"
model_path = f"{root_path}/models"
modelfile_path = f"{root_path}/modelfiles"

if not os.path.exists(modelfile_path):
    os.mkdir(modelfile_path)


# Set model and dataset variables
model_id = "meta-llama/Meta-Llama-3.2-3B-Instruct"

gguf_models = [
    gguf_model 
    for gguf_model in os.listdir(model_path) 
    if os.path.isfile(os.path.join(model_path, gguf_model))
]

datasets = [
    dataset 
    for dataset in os.listdir(static_path) 
    if os.path.isfile(os.path.join(static_path, dataset))
]
