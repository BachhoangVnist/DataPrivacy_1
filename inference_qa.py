if __name__ == "__main__":

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
        DEFAULT_PROMPT_TEMPLATE,
        LLM_MODEL_HUB,
        QLORA_QA_PROMPT_TEMPLATE,
    )
    import time

    # Test environment 
    import langchain
    langchain.verbose = True

    # Bắt đầu đo thời gian
    start_time = time.time()
    # Create LLM model
    llm_model = LLMModel(
        model_name=LLM_MODEL_PATH,
        # model_name=LLM_MODEL_HUB,
        max_new_tokens=2048,
        is_remote_model=False,
    ).llm_model

    # Create embedding model
    embedding_model = EmbeddingModel(model_file=EMBEDDING_MODEL_PATH).embedding_model

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
        k=2
    ).create_qa_chain()

    loop_start_time = time.time()
    # Create question from policy file
    QUESTION = "Dữ liệu cá nhân là gì"
    print('start invoke')
    response = llm_chain.invoke({"query": QUESTION})
    print(response)

    # Kết thúc đo thời gian
    end_time = time.time()
    # Tính thời gian thực thi
    execution_time = end_time - start_time
    print("Tổng thời gian thực thi:", execution_time, "giây")
