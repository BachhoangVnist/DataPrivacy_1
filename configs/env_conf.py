import os
from dotenv import load_dotenv, find_dotenv

# load env
load_dotenv(find_dotenv())
DB_NAME = os.environ.get('DB_NAME')
COLLECTION_NAME = os.environ.get('COLLECTION_NAME')
PRIVACY_POLICY_COLLECTION = os.environ.get('PRIVACY_POLICY_COLLECTION')
MONGODB_PWD = os.environ.get('MONGODB_PWD')
VECTOR_SEARCH_INDEX_NAME = os.environ.get('ATLAS_VECTOR_SEARCH_INDEX_NAME')
HF_TOKEN = os.environ.get('HF_TOKEN')
