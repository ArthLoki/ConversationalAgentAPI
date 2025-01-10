import json
import uuid
import datetime
import requests
from configs import ELASTIC_API_ENDPOINT, ELASTIC_PASSWORD, ELASTIC_USERNAME, mappings
from abort_process import aborting_process

def format_doc(index_name, character_name, conversation_id, question, answer, metadata=None):
    return {
        "index_name": index_name,
        "character": character_name,
        "conversation_id": conversation_id,
        "pair_id": str(uuid.uuid4()),
        "timestamp": datetime.datetime.now(),
        "input": question,
        "output": answer,
        "metadata": metadata or {}
    }


def create_index_elastic(es, index_name, character_name, question, answer, metadata=None):
    es.indices.create(index=index_name, body=mappings)
    conversation_id = str(uuid.uuid4())
    doc = format_doc(index_name, character_name, conversation_id, question, answer)
    try:
        es.index(index=index_name, document=doc)  # Use a dedicated index name
        print(f"Indexed conversation with ID: {conversation_id}\n")
        return conversation_id
    except Exception as e: # Catch and print exceptions for debugging
        print(f"Error indexing document: {e}\n")
        return None


def add_index_elastic(es, index_name, character_name, query, prompt, answer):
    try:
        if not es.indices.exists(index=index_name):
            return None

        resSearch = es.search(index=index_name, query={"match": query})

        conversation_id = resSearch["hits"]["hits"][0]["_source"]["conversation_id"] if len(resSearch["hits"]["hits"]) > 0 else str(uuid.uuid4())
        # this id is static in the same conversation

        new_content = format_doc(index_name, character_name, conversation_id, prompt, answer)

        resAdd = es.index(index=index_name, document=new_content)

        return resAdd
    except Exception as e:
        print(f"Error while adding data in elastic index: {e}")
        return None


def get_index_data(index_name):
    try:
        url = f"{ELASTIC_API_ENDPOINT}/{index_name}/_search"
        auth = (ELASTIC_USERNAME, ELASTIC_PASSWORD) # Tuple with username and password
        headers = {'Content-Type': 'application/json'}

        response =  requests.get(url, auth=auth, headers=headers)
        response_json = json.loads(response.text)["hits"]["hits"]

        return response_json
    except Exception as e:
        print(f"Error while getting elastic index data: {e}")
        return None


def get_previous_messages_from_index_data(es, index_name):

    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=mappings)
        es.indices.refresh(index=index_name)

    list_index_data = get_index_data(index_name)
    if list_index_data == []:
        return []

    previous_messages = []
    for data in list_index_data:
        dictUserMessages = {"role": "user", "content": data["_source"]["input"]}
        dictAssistantMessages = {"role": "assistant", "content": data["_source"]["output"]}
        previous_messages.extend([dictUserMessages, dictAssistantMessages])
    return previous_messages