# Default Variables
OLLAMA_MODEL_NAME = galybel
MODELFILE_FILE = "/mnt/d/vscode/ConversationalAgentAPI/modelfiles/galybel_modelfile"
GGUF_MODEL_NAME = "/mnt/d/vscode/ConversationalAgentAPI/models/v2_galybel_llama3.2.Q8_0.gguf"

# Create model
create-model:
	@echo "Creating model $(OLLAMA_MODEL_NAME) from $(MODELFILE_FILE)..."
	@if [ -f $(MODEL_FILE) ]; then \
		ollama create $(OLLAMA_MODEL_NAME) -f "$(MODELFILE_FILE)"; \
	else \
		echo "Error: Model file $(MODELFILE_FILE) does not exist!"; \
	fi

# Run model
run-model:
	@echo "Running model $(OLLAMA_MODEL_NAME)..."
	ollama run "$(OLLAMA_MODEL_NAME)"

# List models
list-models:
	@echo "Listing models..."
	ollama list
