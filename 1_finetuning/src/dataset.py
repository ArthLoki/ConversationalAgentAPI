from datasets import load_dataset
from transformers import AutoTokenizer
from src.configs import static_path

# Carrega apenas o tokenizer sem alocar o modelo de 3B na GPU
tokenizer = AutoTokenizer.from_pretrained("unsloth/Llama-3.2-3B-Instruct")
EOS_TOKEN = tokenizer.eos_token


def getPromptFormat():
    return "{}"


def formatting_prompts_func(jsonFilename, chatTemplate: str = "chatml"):
    prompt = getPromptFormat()
    texts = []

    if chatTemplate == "alpaca_style":
        instructions = jsonFilename["input"]
        outputs = jsonFilename["output"]
        for instruction, output in zip(instructions, outputs):
            text = prompt.format(output) + EOS_TOKEN
            texts.append(text)
    else:
        messages = jsonFilename["messages"]
        for convo in messages:
            text = tokenizer.apply_chat_template(
                convo, tokenize=False, add_generation_prompt=False
            )
            texts.append(text)

    return {
        "text": texts,
    }


def loadCustomizedDataset(datasetJsonFilename):
    dataset = load_dataset(
        "json",
        data_files=f"{static_path}/chatml/{datasetJsonFilename}.json",
        split="train",
    )
    dataset = dataset.map(
        formatting_prompts_func,
        batched=True,
    )
    return dataset
