from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_core.vectorstores import VectorStore
from langchain_community.llms.ctransformers import CTransformers
from embeddings import EmbeddingModel
from configs import (
    VECTOR_SEARCH_INDEX_NAME,
    DEFAULT_PROMPT_TEMPLATE,
    LLM_MODEL_PATH,
    EMBEDDING_MODEL_PATH,
    LLM_MODEL_HUB,
)
from llms import LLMModel
from prepare_vector_db import MongoDBAtlasVectorSearchBuilder
from mongodb_connector import (
    vietnamese_legal_collection as collection,
)

class RAGQALangChain:

    prompt: PromptTemplate
    llm_model: CTransformers
    vector_database: VectorStore

    def __init__(
            self,
            prompt_template: str,
            llm_model: CTransformers,
            vector_database: VectorStore
        ) -> None:
        self.prompt = self.set_prompt_from_template(
            template=prompt_template
        )
        self.llm_model = llm_model
        self.vector_database = vector_database

    # Create prompt template
    def set_prompt_from_template(
            self,
            template: str = DEFAULT_PROMPT_TEMPLATE
        ) -> PromptTemplate:
        self.prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        return self.prompt

    # Create simple chain
    def create_qa_chain(self):
        llm_chain = RetrievalQA.from_chain_type(
            llm=self.llm_model,
            chain_type="stuff",
            retriever=self.vector_database.as_retriever(
                search_kwargs={
                    "k": 1, 
                }
            ),
            return_source_documents=False,
            chain_type_kwargs={
                'prompt': self.prompt
            }

        )
        return llm_chain

if __name__ == "__main__":
    import time
    # Bắt đầu đo thời gian
    start_time = time.time()
    llm_model = LLMModel(model_file=LLM_MODEL_HUB).llm_model
    embedding_model = EmbeddingModel(model_file=EMBEDDING_MODEL_PATH).embedding_model
    vector_builder = MongoDBAtlasVectorSearchBuilder(
        embedding_model=embedding_model,
        collection=collection,
        vector_search_index_name=VECTOR_SEARCH_INDEX_NAME
    )

    vector_database = vector_builder.get_vector_db()

    llm_chain = RAGQALangChain(
        prompt_template=DEFAULT_PROMPT_TEMPLATE,
        llm_model=llm_model,
        vector_database=vector_database
    ).create_qa_chain()

    # Chay cai chain
    QUESTION = "Quy định về cơ sở vật chất đối với môn đấu kiếm thể thao?"
    print('start invoke')
    response = llm_chain.invoke({"query": QUESTION})
    print(response)

    # Kết thúc đo thời gian
    end_time = time.time()
    # Tính thời gian thực thi
    execution_time = end_time - start_time
    print("Thời gian thực thi:", execution_time, "giây")
