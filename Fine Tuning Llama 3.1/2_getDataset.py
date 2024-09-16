from datasets import load_dataset
import json

EOS_TOKEN = tokenizer.eos_token # Must add EOS_TOKEN


def getPromptFormat():
    return "Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\n\n### Instruction:\n{}\n\n### Response:\n{}"


def formatting_prompts_func(jsonFilename):

    prompt = getPromptFormat()

    instructions = jsonFilename["input"]
    #inputs       = jsonFilename["input"]
    outputs      = jsonFilename["output"]
    texts = []
    for instruction, output in zip(instructions, outputs):
        # Must add EOS_TOKEN, otherwise your generation will go on forever!
        text = prompt.format(instruction, output) + EOS_TOKEN
        texts.append(text)
    return { "text" : texts, }


def loadCustomizedDataset(datasetJsonFilename):
    dataset = load_dataset("json", data_files=datasetJsonFilename, split = "train")
    dataset = dataset.map(formatting_prompts_func, batched = True,)
    print(dataset.column_names)
    return
