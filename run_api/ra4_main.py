from ra3_create_elastic_index import create_index_elastic, add_index_elastic
from abort_process import aborting_process
from ra2_run_ollama_api import run_ollama_model, chose_model
from ra1_connect_elastic import connectElastic

es = connectElastic()

def mainOllamaAPI(index_name):
    try:
        model, character_name = chose_model()

        prompt = input("\nEnter a prompt: ")
        if prompt == "x":
            print('\nYou chose to exit.\n')
            exit(0)

        resResponse = run_ollama_model(es, model, prompt, index_name)
        print("\nAI Response:", resResponse)
        if resResponse is None:
            aborting_process()

        return (character_name, prompt, resResponse)
    except Exception as e:
        print(f"\nError while running main ollama api: {e}")
        exit(0)


def mainElasticIndex(index_name, character_name, prompt, resResponse):
    try:
        if not es.indices.exists(index=index_name):
            create_index_elastic(es, index_name, character_name, prompt, resResponse)
            es.indices.refresh(index=index_name)
            print("Index created successfully!\n")
        else:
            query = {"index_name": index_name} # "index_name": index_name, "character": character_name
            resSearch = es.search(index=index_name, query={"match": query})
            if not resSearch:
                aborting_process()

            resUpdate = add_index_elastic(es, index_name, character_name, query, prompt, resResponse)
            es.indices.refresh(index=index_name)
            if not resUpdate:
                aborting_process()

            print("Index updated successfully!\n")
    except Exception as e:
        print(f"\nError while running main elastic index: {e}")


def main():
    index_name = input("\nEnter an index name to identify conversation: ").lower()

    # Running Ollama Model Using API
    character_name, prompt, resResponse = mainOllamaAPI(index_name)

    # ElasticSearch to create historic messages of each conversation
    mainElasticIndex(index_name, character_name, prompt, resResponse)


if __name__ == "__main__":
    main()
