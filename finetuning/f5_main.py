from f3_finetuning import finetuning  #, inference
from f4_saveModel import save_model
from abort_process import aborting_process


def main():
    # Dataset
    datasetFilename = input("\nWrite the name of the dataset without the extension .json ('x' to exit): ")
    if datasetFilename.lower() == "x":
        aborting_process()

    # Finetuning
    proceed = input("\nDo you want to proceed with the finetuning process? [Y/n] ")
    if proceed.lower() == "n":
        aborting_process()

    print("\nThe finetuning process may take a while...")
    resFinetuning = finetuning(datasetFilename)
    if not resFinetuning:
        aborting_process()
    print(f"\nFinetuning process finished successfully!")

    # # Inference
    # do_inference = input("\nDo you want to do an inference? [Y/n] ")
    # if do_inference.lower() == "n":
    #     aborting_process()

    # print("\nStarting Inference...")
    # playerInput = input("\nEnter an user input: ")
    # resInference = inference(playerInput)
    # if not resInference:
    #     aborting_process()
    # print("\nInference was successfull!")

    # Save Model
    save = input("\nDo you want to save the model? [Y/n] ")
    if save.lower() == "n":
        aborting_process()

    resSave = save_model()
    if not resSave:
        print("\nAn error occured while saving the model.")
        aborting_process()
    print("\nModel saved successfully!")


if __name__ == "__main__":
    main()
