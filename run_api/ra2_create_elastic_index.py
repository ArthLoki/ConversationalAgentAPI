import uuid
import datetime


def format_doc(indexname, conversation_id, question, answer, metadata=None):
    pair_id = str(uuid.uuid4())
    return {
        "indexname": indexname,
        "conversation_id": conversation_id,
        "pair_id": pair_id,
        "timestamp": datetime.datetime.now(),
        "input": question,
        "output": answer,
        "metadata": metadata or {}
    }


def create_index_elastic(es, indexname, question, answer, metadata=None):
    es.indices.create(index=indexname)
    conversation_id = str(uuid.uuid4())
    pair_id = str(uuid.uuid4())
    doc = {
        "indexname": indexname,
        "conversation_id": conversation_id,
        "pair_id": pair_id,
        "timestamp": datetime.datetime.now(),
        "input": question,
        "output": answer,
        "metadata": metadata or {}
    }
    try:
        es.index(index=indexname, document=doc)  # Use a dedicated index name
        print(f"Indexed conversation with ID: {conversation_id}")
        return conversation_id
    except Exception as e: # Catch and print exceptions for debugging
        print(f"Error indexing document: {e}")
        return None


def update_index_elastic(es, indexname, query, prompt, answer):
    try:
        if not es.indices.exists(index=indexname):
            return None

        resSearch = es.search(index=indexname, body=query)
        print(resSearch)

        new_content = format_doc(indexname, resSearch["conversation_id"], prompt, answer)

        return es.update(index=indexname, id=resSearch["conversation_id"], doc=new_content)
    except Exception as e:
        print(f"Error while updating elastic index: {e}")
        return None
