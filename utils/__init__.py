import time
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# pylint: disable=wrong-import-position
from sentence_transformers import util
from embeddings import embedding_model
from utils.path_utils import (
    BasePathUtils,
    PathUtils
)
def get_embedding(query: str):
    return embedding_model.embed_query(query)

def merge_arrays_to_objects(texts: list, embedding_vectors: list) -> list:
    merged_objects = []
    if len(texts) != len(embedding_vectors):
        print("Error not len text and embedding vectors not qual !")

        return merged_objects

    for text, number in zip(texts, embedding_vectors):
        merged_object = {"text": text, "embedding": number}
        merged_objects.append(merged_object)

    return merged_objects

def calculate_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print("Thời gian thực thi của", func.__name__, ":", execution_time, "giây")
        return result
    return wrapper

def caculate_sentence_similarity(vector_1: list, vector_2: list):
    return util.pytorch_cos_sim(vector_1, vector_2)

if __name__ == "__main__":
    DIRECTORY_PATH = "data"
    path_util = PathUtils()
    paths = path_util.create_file_path_in_current_directory(foler_name=DIRECTORY_PATH, file_name="data.csv")
    print("Các file CSV trong thư mục:")
    print(paths)
