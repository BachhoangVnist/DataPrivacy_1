import os
from dotenv import load_dotenv, find_dotenv

# load env
load_dotenv(find_dotenv())
DB_NAME = os.environ.get('DB_NAME')
COLLECTION_NAME = os.environ.get('COLLECTION_NAME')
MONGODB_PWD = os.environ.get('MONGODB_PWD')
VECTOR_SEARCH_INDEX_NAME = os.environ.get('ATLAS_VECTOR_SEARCH_INDEX_NAME')
