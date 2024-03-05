from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_core.vectorstores import VectorStore
from langchain_mongodb import MongoDBAtlasVectorSearch
from embeddings import embedding_model
from mongodb_connector import vietnamese_legal_collection
from configs import VECTOR_SEARCH_INDEX_NAME
from llms import llm_model

# Tao prompt template
def creat_prompt(template):
    prompt = PromptTemplate(template = template, input_variables=["context", "question"])
    return prompt

# Tao simple chain
def create_qa_chain(prompt, llm, db: VectorStore):
    llm_chain = RetrievalQA.from_chain_type(
        llm = llm,
        chain_type= "stuff",
        retriever = db.as_retriever(search_kwargs = {
            "k":1, }),
        return_source_documents = False,
        chain_type_kwargs= {'prompt': prompt}

    )
    return llm_chain

# Read from VectorDB
def read_vectors_db():
    vectorStore = MongoDBAtlasVectorSearch(
        vietnamese_legal_collection,
        embedding_model,
        index_name=VECTOR_SEARCH_INDEX_NAME
    )
    return vectorStore

if __name__ == "__main__":
    # Bat dau thu nghiem
    # db = read_vectors_db()
    # output = db.similarity_search_with_score(query="Quy định về cơ sở vật chất đối với môn đấu kiếm thể thao?", 
    #                                          k=2,
    #                                          post_filter_pipeline=  [
    #                                             {
    #                                                 "$project": {
    #                                                     "_id": 0,
    #                                                     "text": 1, 
    #                                                     "score": { "$meta": "vectorSearchScore" }
    #                                                 }
    #                                             }],)
    # print(output)

    import time
    # Bắt đầu đo thời gian
    start_time = time.time()

    db = read_vectors_db()
    #Tao Prompt
    template = """<|im_start|>system\nSử dụng thông tin sau đây để trả lời câu hỏi. Nếu bạn không biết câu trả lời, hãy nói không biết, đừng cố tạo ra câu trả lời\n
        {context}<|im_end|>\n<|im_start|>user\n{question}<|im_end|>\n<|im_start|>assistant"""
    prompt = creat_prompt(template)

    llm_chain  =create_qa_chain(prompt, llm_model, db)

    # Chay cai chain
    question = "Quy định về cơ sở vật chất đối với môn đấu kiếm thể thao?"
    print('start invoke')
    response = llm_chain.invoke({"query": question})
    print(response)

    # Kết thúc đo thời gian
    end_time = time.time()
    # Tính thời gian thực thi
    execution_time = end_time - start_time
    print("Thời gian thực thi:", execution_time, "giây")
