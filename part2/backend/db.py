import os
from pymongo import MongoClient
from dotenv import load_dotenv
from pymongo.server_api import ServerApi

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError(
        "MONGO_URI is not set. Copy .env.example to .env and fill in the value."
    )

client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client.get_default_database()
