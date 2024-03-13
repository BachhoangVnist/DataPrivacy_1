from argparse import ArgumentParser
import time
import langchain

from ragqa_langchain import RAGQALangChain
from llms import LLMModel
from embeddings import EmbeddingModel
from prepare_vector_db import (
    MongoDBAtlasVectorSearchBuilder,
)
from mongodb_connector import (
    vietnamese_legal_collection as legal_collection,
)
from configs import (
    LLM_MODEL_PATH,
    EMBEDDING_MODEL_PATH,
    VECTOR_SEARCH_INDEX_NAME,
    QLORA_QA_PROMPT_TEMPLATE,
    APP_DEBUG,
)

def main(
        question: str,
        model_name: str = None,
        embedding_model_name: str = None,
        k_nearest: str = None,
    ) -> None:

    if model_name is None:
        model_name = LLM_MODEL_PATH

    if embedding_model_name is None:
        embedding_model_name = EMBEDDING_MODEL_PATH

    if k_nearest is None:
        k_nearest = 3
    else:
        try:
            k_nearest = int(k_nearest)
        except ValueError as e:
            raise ValueError("Please enter a valid integer.") from e

    langchain.verbose = APP_DEBUG

    # Start measuring time
    start_time = time.time()
    # Create LLM model
    llm_model = LLMModel(
        model_name=model_name,
        max_new_tokens=2048,
        is_remote_model=False,
    ).get_llm_model()

    # Create embedding model
    embedding_model = EmbeddingModel(
        model_name=embedding_model_name
    ).get_embedding_model()

    # Create vector builder mongodb and local faiss
    mongo_vector_builder = MongoDBAtlasVectorSearchBuilder(
        embedding_model=embedding_model,
        collection=legal_collection,
        vector_search_index_name=VECTOR_SEARCH_INDEX_NAME,
    )

    # Create LLM chain
    mongo_vector_database = mongo_vector_builder.get_vector_db()
    llm_chain = RAGQALangChain(
        prompt_template=QLORA_QA_PROMPT_TEMPLATE,
        llm_model=llm_model,
        vector_database=mongo_vector_database,
        k=k_nearest
    ).create_qa_chain()

    print("start invoke")
    response = llm_chain.invoke({"query": question})
    print(response)

    # End of time measurement
    end_time = time.time()
    # Calculate execution time
    execution_time = end_time - start_time
    print("Total execution time:", execution_time, "s")


if __name__ == "__main__":
    # Add arguments
    parser = ArgumentParser()
    parser.add_argument("-q", "--query", dest="question", help="Please specify the question", metavar="str")
    parser.add_argument("-m", "--model", dest="model_name", default=None, metavar="str")
    parser.add_argument("-e", "--embedding", dest="embedding", default=None, metavar="str")
    parser.add_argument("-k", "--k-nearest", dest="k_nearest", default=None, metavar="int")
    # Analyze the arguments
    args = parser.parse_args()

    main(
        question=args.question,
        model_name=args.model_name,
        embedding_model_name=args.embedding,
        k_nearest=args.k_nearest
    )
