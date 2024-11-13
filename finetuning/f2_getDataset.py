from datasets import load_dataset
import json

from f1_getModel import getBaseModelAndTokenizer

_, tokenizer = getBaseModelAndTokenizer()
EOS_TOKEN = tokenizer.eos_token # Must add EOS_TOKEN
dataset_loc = "static/"


def getPromptFormat():
    return "Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\n\n### Instruction:\n{}\n\n### Response:\n{}"


def formatting_prompts_func(jsonFilename):

    prompt = getPromptFormat()
    # instructions = jsonFilename.get("input", [])
    # outputs = jsonFilename.get("output", [])

    # if instructions is None or outputs is None:
    #     return { "text": [] }  # Return an empty list if missing data

    instructions = jsonFilename["input"]
    outputs = jsonFilename["output"]
    texts = []
    for instruction, output in zip(instructions, outputs):
        # Must add EOS_TOKEN, otherwise your generation will go on forever!
        text = prompt.format(instruction, output) + EOS_TOKEN
        texts.append(text)
    return { "text" : texts, }


def loadCustomizedDataset(datasetJsonFilename):
    dataset = load_dataset("json", data_files=f"{dataset_loc}/{datasetJsonFilename}.json", split="train")
    dataset = dataset.map(formatting_prompts_func, batched = True,)
    return dataset
