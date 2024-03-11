from pymongo import MongoClient
from configs import (
    MONGODB_PWD as PASSWORD,
    DB_NAME,
    COLLECTION_NAME
)

# connect serve
connection_string = f'mongodb+srv://0606bach:{PASSWORD}@cluster0.vc1gtc4.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(connection_string)

# export
embedding_db = client[DB_NAME]
vietnamese_legal_collection = embedding_db[COLLECTION_NAME]
