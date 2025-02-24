from trl import SFTTrainer
from transformers import TrainingArguments  #, TextStreamer
from unsloth import is_bfloat16_supported  #, FastLanguageModel
import torch



from f1_getModel import getBaseModelAndTokenizer, getMaxSeqLength
from f2_getDataset import loadCustomizedDataset, getPromptFormat

global max_seq_length, prompt
max_seq_length = getMaxSeqLength()
prompt = getPromptFormat()


def getTrainer(model, tokenizer, dataset):

    try:
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
    except Exception as err:
        print("\nError while setting trainer: ", err)
        return


def train(model, tokenizer, dataset):
    print("\n>>> TRAINER")
    print("Set trainer.")
    trainer = getTrainer(model, tokenizer, dataset)
    if trainer is None:
        return False
    print("The trainer was set successfuly")

    try:
        print("\n>>> TRAINING")
        print("Starting Training...")
        trainer.train()
        print("Training finished...")
        return True
    except Exception as err:
        print("Error while training: ", err)
        return False


# def inference(model, tokenizer, instruction: str):
#     FastLanguageModel.for_inference(model) # Enable native 2x faster inference
#     inputs = tokenizer(
#     [
#         prompt.format(
#             instruction, # instruction
#             "", # input
#             "", # output - leave this blank for generation!
#         )
#     ], return_tensors = "pt").to("cuda")

#     text_streamer = TextStreamer(tokenizer)
#     _ = model.generate(**inputs, streamer = text_streamer, max_new_tokens = 128)
#     return True


def finetuning(datasetJSONFilename):
    model, tokenizer = getBaseModelAndTokenizer()
    dataset = loadCustomizedDataset(datasetJSONFilename)
    resTrain = train(model, tokenizer, dataset)
    if not resTrain:
        return False
    return True
