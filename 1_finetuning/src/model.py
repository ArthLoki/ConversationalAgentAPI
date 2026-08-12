from unsloth import FastLanguageModel

# import torch

max_seq_length = 2048  # Choose any! We auto support RoPE Scaling internally!
dtype = (
    None  # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
)
load_in_4bit = True  # Use 4bit quantization to reduce memory usage. Can be False.


def getMaxSeqLength():
    return max_seq_length


def getBaseModelAndTokenizer():
    # 4bit pre quantized models we support for 4x faster downloading + no OOMs.
    # fourbit_models = [
    #     "unsloth/mistral-7b-v0.3-bnb-4bit",      # New Mistral v3 2x faster!
    #     "unsloth/mistral-7b-instruct-v0.3-bnb-4bit",
    #     "unsloth/llama-3-8b-bnb-4bit",           # Llama-3 15 trillion tokens model 2x faster!
    #     "unsloth/llama-3-8b-Instruct-bnb-4bit",
    #     "unsloth/llama-3-70b-bnb-4bit",
    #     "unsloth/Phi-3-mini-4k-instruct",        # Phi-3 2x faster!
    #     "unsloth/Phi-3-medium-4k-instruct",
    #     "unsloth/mistral-7b-bnb-4bit",
    #     "unsloth/gemma-7b-bnb-4bit",             # Gemma 2.2x faster!
    # ] # More models at https://huggingface.co/unsloth

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="unsloth/Llama-3.2-3B-Instruct",  # "unsloth/Ministral-3-3B-Instruct-2512-GGUF", # "unsloth/Llama-3.2-3B-Instruct",
        max_seq_length=max_seq_length,
        dtype=dtype,
        load_in_4bit=load_in_4bit,
        # token = "hf_...", # use one if using gated models like meta-llama/Llama-2-7b-hf
        # chat_template = "llama-3.1"  # "mistral"
    )

    model = FastLanguageModel.get_peft_model(
        model,
        r=16,  # Choose any number > 0 ! Suggested 8, 16, 32, 64, 128
        target_modules=[
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
            "gate_proj",
            "up_proj",
            "down_proj",
        ],
        lora_alpha=16,
        lora_dropout=0,  # Supports any, but = 0 is optimized
        bias="none",  # Supports any, but = "none" is optimized
        # [NEW] "unsloth" uses 30% less VRAM, fits 2x larger batch sizes!
        use_gradient_checkpointing="unsloth",  # True or "unsloth" for very long context
        random_state=3407,
        use_rslora=False,  # We support rank stabilized LoRA
        loftq_config=None,  # And LoftQ
    )

    return (model, tokenizer)


def save_lora_model(model, tokenizer, folder_name="lora_model"):
    """Salva os adaptadores LoRA (~50MB) - Leve e garantido."""
    try:
        model.save_pretrained(folder_name)
        tokenizer.save_pretrained(folder_name)
        print(f"LoRA model successfully saved to '{folder_name}'")
        return True
    except Exception as err:
        print(f"Error while saving LoRA model: {err}")
        return False


def save_gguf_model(model, tokenizer, folder_name="model", quantization="q4_k_m"):
    """Tenta converter e salvar diretamente em GGUF."""
    try:
        model.save_pretrained_gguf(
            folder_name,
            tokenizer,
            quantization_method=quantization,
        )
        print(f"GGUF model successfully saved to '{folder_name}'")
        return True
    except Exception as err:
        print(f"Error while saving GGUF model: {err}")
        return False


def save_model(model, tokenizer):
    """Recebe o modelo JÁ TREINADO e o tokenizer para salvar."""
    # 1. Salva sempre o LoRA como backup garantido
    lora_saved = save_lora_model(model, tokenizer)

    # 2. Tenta o salvamento GGUF
    gguf_saved = save_gguf_model(model, tokenizer)

    return lora_saved or gguf_saved
