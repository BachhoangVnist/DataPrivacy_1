import time
from argparse import ArgumentParser
import langchain

from privacy_policy_processor import PrivacyPolicyProcessor
from ragqa_langchain import RAGQALangChain
from llms import LLMModel
from embeddings import EmbeddingModel
from prepare_vector_db import (
    MongoDBAtlasVectorSearchBuilder,
    FAISSVectorSearchBuilder
)

from configs import (
    LLM_MODEL_PATH,
    EMBEDDING_MODEL_PATH,
    VECTOR_SEARCH_INDEX_NAME,
    DEFAULT_PROMPT_TEMPLATE,
    APP_DEBUG
)

# pylint: disable=unused-import
from controllers import PrivacyPolicyController
from mongodb_connector import (
    vietnamese_legal_collection as legal_collection,
    privacy_policy_collection as privacy_collection
)
# pylint: disable=too-many-locals
def main(
        url_path: str,
        model_name: str = None,
        embedding_model_name: str = None,
        k_nearest_legal: str = None,
        k_nearest_policy: str = None,
    ) -> None:

    if model_name is None:
        model_name = LLM_MODEL_PATH

    if embedding_model_name is None:
        embedding_model_name = EMBEDDING_MODEL_PATH

    if k_nearest_legal is None:
        k_nearest_legal = 3
    else:
        try:
            k_nearest_legal = int(k_nearest_legal)
        except ValueError as e:
            raise ValueError("Please enter a valid integer.") from e

    if k_nearest_policy is None:
        k_nearest_policy = 3
    else:
        try:
            k_nearest_policy = int(k_nearest_policy)
        except ValueError as e:
            raise ValueError("Please enter a valid integer.") from e

    langchain.verbose = APP_DEBUG

    # Bắt đầu đo thời gian
    start_time = time.time()
    # Create LLM model
    llm_model = LLMModel(
        model_name=model_name
    ).get_llm_model()

    # Create embedding model
    embedding_model = EmbeddingModel(
        model_name=embedding_model_name
    ).get_embedding_model()

    # Create vector builder mongodb and local faiss
    mongo_vector_builder = MongoDBAtlasVectorSearchBuilder(
        embedding_model=embedding_model,
        collection=legal_collection,
        vector_search_index_name=VECTOR_SEARCH_INDEX_NAME
    )
    local_vector_builder = FAISSVectorSearchBuilder(
        embedding_model=embedding_model,
    )

    # Create LLM chain
    mongo_vector_database = mongo_vector_builder.get_vector_db()
    llm_chain = RAGQALangChain(
        prompt_template=DEFAULT_PROMPT_TEMPLATE,
        llm_model=llm_model,
        vector_database=mongo_vector_database,
        k=k_nearest_legal
    ).create_qa_chain()

    # # Get all policy privacy document
    # privacy_controller = PrivacyPolicyController(
    #     collection=privacy_collection
    # )
    # policy_documents = privacy_controller.read_all_documents()
    # for policy in policy_documents:
    #     loop_start_time = time.time()
    #     print(policy)
    #     # Create question from policy file
    #     privacy_policy_processor = PrivacyPolicyProcessor(
    #         policy_url=policy["policy_path"],
    #         vector_builder=local_vector_builder
    #     )
    #     QUESTION = privacy_policy_processor.process()
    #     print("start invoke")
    #     response = llm_chain.invoke({"query": QUESTION})
    #     print(response)
    #     loop_end_time = time.time()
    #     loop_execution_time = loop_end_time - loop_start_time
    #     print("Thời gian thực thi:", loop_execution_time, "giây")

    #     data = policy
    #     data["response_time"] = loop_execution_time
    #     data["result"] = response["result"]
    #     privacy_controller.update_document_by_id(
    #         document_id=policy["_id"],
    #         data=data
    #     )

    print(url_path)
    # Create question from policy file
    privacy_policy_processor = PrivacyPolicyProcessor(
        policy_url=url_path,
        vector_builder=local_vector_builder,
        k=k_nearest_policy
    )
    question = privacy_policy_processor.process()
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
    parser.add_argument("-u", "--url", dest="url_path", help="Please specify the url path", metavar="str")
    parser.add_argument("-m", "--model", dest="model_name", default=None, metavar="str")
    parser.add_argument("-e", "--embedding", dest="embedding", default=None, metavar="str")
    parser.add_argument("-l", "--k-nearest-legal", dest="k_nearest_legal", default=None, metavar="int")
    parser.add_argument("-p", "--k-nearest-policy", dest="k_nearest_policy", default=None, metavar="int")
    # Analyze the arguments
    args = parser.parse_args()

    main(
        url_path=args.url_path,
        model_name=args.model_name,
        embedding_model_name=args.embedding,
        k_nearest_legal=args.k_nearest_legal,
        k_nearest_policy=args.k_nearest_policy
    )
