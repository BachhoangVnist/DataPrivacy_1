import os
import time
from sentence_transformers import util

def merge_arrays_to_objects(texts: list, embedding_vectors: list) -> list:
    merged_objects = []
    if len(texts) != len(embedding_vectors):
        print("Error not len text and embedding vectors not qual !")

        return merged_objects

    for text, number in zip(texts, embedding_vectors):
        merged_object = {"text": text, "embedding": number}
        merged_objects.append(merged_object)

    return merged_objects

def get_csv_files_in_directory(directory):
    csv_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            csv_files.append(os.path.join(directory, filename))
    return csv_files

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

def create_file_path_in_current_directory(foler_name: str, file_name: str) -> str:
    # Use the current_directory variable to create the path to the file in the current working directory
    current_directory = os.getcwd()

    # Create file_path by joining the current_directory and file_name
    folder_path = os.path.join(current_directory, foler_name)
    # If folder name not exit create folder
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, file_name)
    return file_path

if __name__ == "__main__":
    DIRECTORY_PATH = "data"
    csv_files = get_csv_files_in_directory(DIRECTORY_PATH)
    print("Các file CSV trong thư mục:")
    for csv_file in csv_files:
        print(csv_file)
