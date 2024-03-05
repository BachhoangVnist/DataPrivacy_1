from langchain_community.llms import CTransformers
from typing import Optional

class LLMModel:
    model_file: str
    embedding_model: Optional[CTransformers]

    def __init__(self, model_file: str):
        self.model_file = model_file
        self.llm_model = self.load_llm()

    # Load LLM
    def load_llm(self) -> Optional[CTransformers]:
        llm = CTransformers(
            model=self.model_file,
            model_type="llama",
            max_new_tokens=1024,
            temperature=0.01
        )
        return llm
