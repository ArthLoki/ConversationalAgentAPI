from f1_getModel import getBaseModelAndTokenizer


# def save_lora_model(model, tokenizer):
#     model.save_pretrained("lora_model") # Local saving
#     tokenizer.save_pretrained("lora_model")


def save_model():
    try:
        model, tokenizer = getBaseModelAndTokenizer()
        # save_lora_model(model, tokenizer)
        model.save_pretrained_gguf("model", tokenizer,)
        return True
    except Exception as err:
        print(f"Error while saving model: {err}")
        return False
