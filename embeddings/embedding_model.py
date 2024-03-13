from typing import Optional
from langchain_community.embeddings import HuggingFaceEmbeddings

class EmbeddingModel:
    __model_name: str
    __embedding_model: Optional[HuggingFaceEmbeddings]

    def __init__(self, model_name: str):
        self.__model_name = model_name
        self.__embedding_model = self.__load_embedding()

    # Load embedding
    def __load_embedding(self) -> Optional[HuggingFaceEmbeddings]:
        # Embedding
        embedding_model = HuggingFaceEmbeddings(
            model_name=self.__model_name
        )
        return embedding_model

    def get_embedding_model(self) -> Optional[HuggingFaceEmbeddings]:
        return self.__embedding_model

    def get_model_name(self) -> str:
        return self.__model_name
