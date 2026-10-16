import torch
import gc
from unsloth import FastLanguageModel

# Libera memória residual do PyTorch
gc.collect()
torch.cuda.empty_cache()

# Carrega o modelo com os adaptadores LoRA salvos
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="lora_model",
    max_seq_length=2048,
    load_in_4bit=True,
)

# Salva mesclando os pesos para o formato HuggingFace primeiro
model.save_pretrained_merged("merged_model", tokenizer, save_method="merged_16bit")
print("Modelo mesclado com sucesso em 'merged_model'!")
