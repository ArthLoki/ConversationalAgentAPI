from src.finetuning import *
from src.model import *
from src.abort_process import *


def main():
    # Dataset
    datasetFilename = input(
        "\nWrite the name of the dataset without the extension .json ('x' to exit): "
    )
    if datasetFilename.lower() == "x":
        aborting_process()

    # Finetuning
    proceed = input("\nDo you want to proceed with the finetuning process? [Y/n] ")
    if proceed.lower() == "n":
        aborting_process()

    print("\nThe finetuning process may take a while...")
    model, tokenizer = finetuning(datasetFilename)
    if model is None or tokenizer is None:
        aborting_process()
    print(f"\nFinetuning process finished successfully!")

    # Save Model
    save = input("\nDo you want to save the model? [Y/n] ")
    if save.lower() == "n":
        aborting_process()

    resSave = save_model(model, tokenizer)
    if not resSave:
        print("\nAn error occured while saving GGUF model.")
        aborting_process()
    print("\nModel saved successfully!")


if __name__ == "__main__":
    main()
