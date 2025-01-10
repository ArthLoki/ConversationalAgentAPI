import os
from dotenv import load_dotenv

load_dotenv()

ELASTIC_API_KEY = os.getenv("ELASTIC_API_KEY")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_API_ENDPOINT = os.getenv("ELASTIC_API_ENDPOINT")

mappings = {
    "mappings": {
        "properties": {
            "index_name": {"type": "text"},
            "character": {"type": "text"},
            "conversation_id": { "type": "keyword" },
            "pair_id": { "type": "keyword" },
            "timestamp": { "type": "date" },
            "input": { "type": "text" },
            "output": { "type": "text" },
            "metadata": { "type": "object" }
        }
    }
}
