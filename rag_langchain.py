from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_core.vectorstores import VectorStore
from langchain_community.llms.ctransformers import CTransformers
import langchain
from embeddings import EmbeddingModel
from configs import (
    VECTOR_SEARCH_INDEX_NAME,
    DEFAULT_PROMPT_TEMPLATE,
    LLM_MODEL_PATH,
    EMBEDDING_MODEL_PATH,
    APP_DEBUG,
)
from llms import LLMModel
from prepare_vector_db import (
    MongoDBAtlasVectorSearchBuilder,
    FAISSVectorSearchBuilder
)
from mongodb_connector import (
    vietnamese_legal_collection as collection,
)
class RAGLangChain:

    prompt: PromptTemplate
    llm_model: CTransformers
    vector_database: VectorStore
    k: int

    def __init__(
            self,
            prompt_template: str,
            llm_model: CTransformers,
            vector_database: VectorStore,
            k: int = 5,
        ) -> None:
        """
        Initializes the object with the provided prompt template,
            language model, vector database, and optional k value.

        Parameters:
            prompt_template (str): The template for the prompt.
            llm_model (CTransformers): The language model.
            vector_database (VectorStore): The vector database.
            k (int, optional): The value for k. Defaults to 5.

        Returns:
            None
        """
        self.prompt = self.set_prompt_from_template(
            template=prompt_template
        )
        self.llm_model = llm_model
        self.vector_database = vector_database
        self.k = k

    # Create prompt template
    def set_prompt_from_template(
            self,
            template: str = DEFAULT_PROMPT_TEMPLATE
        ) -> PromptTemplate:
        """
        Set prompt from template.

        :param template: The prompt template to set.
        :type template: str
        :return: The prompt template object that was set.
        :rtype: PromptTemplate
        """
        self.prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )

        return self.prompt

    # Create simple chain
    def create_qa_chain(self, k: int = None):
        """
        Create a QA chain using the specified k value,
            or the default value if k is None. 
        Return the generated QA chain.
        """
        if k is None:
            k = self.k

        llm_chain = RetrievalQA.from_chain_type(
            llm=self.llm_model,
            chain_type="stuff",
            retriever=self.vector_database.as_retriever(
                search_kwargs={
                    "k": k,
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
    langchain.verbose = APP_DEBUG
    start_time = time.time()
    # Create LLM model
    llm_model = LLMModel(
        model_name=LLM_MODEL_PATH
    ).get_llm_model()

    # Create embedding model
    embedding_model = EmbeddingModel(
        model_name=EMBEDDING_MODEL_PATH
    ).get_embedding_model()

    # Create vector builder mongodb and local faiss
    mongo_vector_builder = MongoDBAtlasVectorSearchBuilder(
        embedding_model=embedding_model,
        collection=collection,
        vector_search_index_name=VECTOR_SEARCH_INDEX_NAME
    )
    local_vector_builder = FAISSVectorSearchBuilder(
        embedding_model=embedding_model,
    )

    # Create LLM chain
    mongo_vector_database = mongo_vector_builder.get_vector_db()
    llm_chain = RAGLangChain(
        prompt_template=DEFAULT_PROMPT_TEMPLATE,
        llm_model=llm_model,
        vector_database=mongo_vector_database
    ).create_qa_chain()

    QUESTION = "Dữ liệu cá nhân bao gồm"

    print('start invoke')
    response = llm_chain.invoke({"query": QUESTION})
    print(response)

    # Kết thúc đo thời gian
    end_time = time.time()
    # Tính thời gian thực thi
    execution_time = end_time - start_time
    print("Thời gian thực thi:", execution_time, "giây")
