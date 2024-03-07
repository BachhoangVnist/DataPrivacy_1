if __name__ == "__main__":

    from privacy_policy_processor import PrivacyPolicyProcessor
    from ragqa_langchain import RAGQALangChain
    from llms import LLMModel
    from embeddings import EmbeddingModel
    from prepare_vector_db import (
        MongoDBAtlasVectorSearchBuilder,
        FAISSVectorSearchBuilder
    )
    from mongodb_connector import (
        vietnamese_legal_collection as legal_collection,
        privacy_policy_collection as privacy_collection
    )
    from configs import (
        LLM_MODEL_PATH,
        EMBEDDING_MODEL_PATH,
        VECTOR_SEARCH_INDEX_NAME,
        DEFAULT_PROMPT_TEMPLATE
    )
    from controllers import PrivacyPolicyController
    import time

    # Test environment 
    import langchain
    langchain.verbose = True

    # Bắt đầu đo thời gian
    start_time = time.time()
    # Create LLM model
    llm_model = LLMModel(model_name=LLM_MODEL_PATH).llm_model

    # Create embedding model
    embedding_model = EmbeddingModel(model_file=EMBEDDING_MODEL_PATH).embedding_model

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
        k=3
    ).create_qa_chain()

    # Get all policy privacy document
    privacy_controller = PrivacyPolicyController(
        collection=privacy_collection
    )
    policy_documents = privacy_controller.read_all_documents()
    for policy in policy_documents:
        loop_start_time = time.time()
        print(policy)
        # Create question from policy file
        privacy_policy_processor = PrivacyPolicyProcessor(
            policy_url=policy["policy_path"],
            vector_builder=local_vector_builder
        )
        QUESTION = privacy_policy_processor.process()
        print('start invoke')
        response = llm_chain.invoke({"query": QUESTION})
        print(response)
        loop_end_time = time.time()
        loop_execution_time = loop_end_time - loop_start_time
        print("Thời gian thực thi:", loop_execution_time, "giây")

        data = policy
        data["response_time"] = loop_execution_time
        data["result"] = response["result"]
        privacy_controller.update_document_by_id(
            document_id=policy["_id"],
            data=data
        )

    # Kết thúc đo thời gian
    end_time = time.time()
    # Tính thời gian thực thi
    execution_time = end_time - start_time
    print("Tổng thời gian thực thi:", execution_time, "giây")
