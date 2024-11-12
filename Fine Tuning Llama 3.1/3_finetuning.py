from trl import SFTTrainer
from transformers import TrainingArguments, TextStreamer
from unsloth import is_bfloat16_supported
import torch

from getModel import getBaseModelAndTokenizer, getMaxSeqLength
from getDataset import loadCustomizedDataset, getPromptFormat

global max_seq_length, prompt
max_seq_length = getMaxSeqLength()
prompt = getPromptFormat()


def getTrainer(model, tokenizer, dataset):
    trainer = SFTTrainer(
        model = model,
        tokenizer = tokenizer,
        train_dataset = dataset,
        dataset_text_field = "text",
        max_seq_length = max_seq_length,
        dataset_num_proc = 2,
        packing = False, # Can make training 5x faster for short sequences.
        args = TrainingArguments(
            per_device_train_batch_size = 2,
            gradient_accumulation_steps = 4,
            warmup_steps = 5,
            max_steps = 60,
            #num_train_epochs = 60, # For longer training runs!
            learning_rate = 2e-4,
            fp16 = not is_bfloat16_supported(),
            bf16 = is_bfloat16_supported(),
            logging_steps = 1,
            optim = "adamw_8bit",
            weight_decay = 0.01,
            lr_scheduler_type = "linear",
            seed = 3407,
            output_dir = "outputs",
        ),
    )

    return trainer


def train(model, tokenizer, dataset):
    try:
        trainer_stats = trainer.train()
        return
    except Exception as e:
        print("Error while training: ", e)
        exit(1)


def inference(prompt):
    FastLanguageModel.for_inference(model) # Enable native 2x faster inference
    inputs = tokenizer(
    [
        prompt.format(
            "Mago, minha espada está brilhando. O que é isso?", # instruction
            "", # input
            "", # output - leave this blank for generation!
        )
    ], return_tensors = "pt").to("cuda")

    text_streamer = TextStreamer(tokenizer)
    _ = model.generate(**inputs, streamer = text_streamer, max_new_tokens = 128)
    return


def main():
    return