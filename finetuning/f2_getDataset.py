from datasets import load_dataset
import json

from f1_getModel import getBaseModelAndTokenizer
from configs import static_path

_, tokenizer = getBaseModelAndTokenizer()
EOS_TOKEN = tokenizer.eos_token # Must add EOS_TOKEN


def getPromptFormat():
    return "{}"


def formatting_prompts_func(jsonFilename):

    prompt = getPromptFormat()

    instructions = jsonFilename["input"]
    outputs = jsonFilename["output"]
    texts = []
    for instruction, output in zip(instructions, outputs):
        # Must add EOS_TOKEN, otherwise your generation will go on forever!
        text = prompt.format(output) + EOS_TOKEN
        texts.append(text)
    return { "text" : texts, }


def loadCustomizedDataset(datasetJsonFilename):
    dataset = load_dataset("json", data_files=f"{static_path}/{datasetJsonFilename}.json", split="train")
    dataset = dataset.map(formatting_prompts_func, batched = True,)
    return dataset
