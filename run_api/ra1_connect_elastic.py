from elasticsearch import Elasticsearch
from configs import ELASTIC_API_ENDPOINT, ELASTIC_API_KEY
from abort_process import aborting_process


def connectElastic():
    try:
        es = Elasticsearch(
            ELASTIC_API_ENDPOINT,
            api_key=ELASTIC_API_KEY
        )

        if es.ping():
            print("Connected to Elasticsearch")
        else:
            raise ConnectionError("Could not connect to Elasticsearch")

        return es
    except ConnectionError as e:
        print(f"Connection Error: {e}\n")
        aborting_process()
