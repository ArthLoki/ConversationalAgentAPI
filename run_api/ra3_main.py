from elasticsearch import Elasticsearch
from ra2_create_elastic_index import create_index_elastic, update_index_elastic
from abort_process import aborting_process
from ra1_run_ollama_api import run_ollama_model, list_models

# Elasticsearch connection (replace with your settings)
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])


def mainOllamaAPI():
    try:
        models_available = list_models()
        print(models_available)

        model_key = input("\nChoose a model to run (only the numeric value): ")
        model = models_available.get(str(model_key))

        if model == None:
            print("\nThe selected model doesn't exist.\n")
            aborting_process()

        prompt = input("\nEnter a prompt: ")
        if prompt == "x":
            print('\nYou chose to exit.\n')
            exit(0)

        resResponse = run_ollama_model(model, prompt)
        print("\nAI Response:", resResponse)
        if resResponse is None:
            aborting_process()

        return (prompt, resResponse)
    except Exception as e:
        print(f"\nError while running main ollama api: {e}")
        exit(0)


def mainElasticIndex(prompt, resResponse):
    try:
        indexname = input("\nEnter an index name to identify conversation: ")
        if not es.indices.exists(index=indexname):
            create_index_elastic(es, indexname, prompt, resResponse)

        resSearch = es.search(index=indexname, body={"indexname": indexname})
        print(resSearch)
        if not resSearch:
            aborting_process()

        query = {"indexname": indexname}
        resUpdate = update_index_elastic(es, indexname, query, prompt, resResponse)
        print(resUpdate)
        if not resUpdate:
            aborting_process()
    except Exception as e:
        print(f"\nError while running main elastic index: {e}")
        exit(0)


def main():
    # Running Ollama Model Using API
    prompt, resResponse = mainOllamaAPI()

    # ElasticSearch to create historic messages of each conversation
    # mainElasticIndex(prompt, resResponse)

    return resResponse


if __name__ == "__main__":
    main()
