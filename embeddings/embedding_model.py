from typing import Optional
from langchain_community.embeddings import HuggingFaceEmbeddings

class EmbeddingModel:
    model_file: str
    embedding_model: Optional[HuggingFaceEmbeddings]

    def __init__(self, model_file: str):
        self.model_file = model_file
        self.embedding_model = self.load_embedding()

    # Load embedding
    def load_embedding(self) -> Optional[HuggingFaceEmbeddings]:
        # Embedding
        embedding_model = HuggingFaceEmbeddings(
            model_name=self.model_file
        )
        return embedding_model
