# uncomment to test

#----------------------------------------------------------------------------------------
# from datasets_controller import (
#     find_similar_documents
# )
# test get similar documents
# QUERY = "Điều 9 15/2019/QĐ-UBND ban hành quy định tiêu chuẩn chức danh lãnh đạo"
# embedding_query = get_embedding(query=QUERY)
# similar_documents = find_similar_documents(embedding=embedding_query)
# for doc in similar_documents:
#     print(doc)

#----------------------------------------------------------------------------------------

# Test similarity vector score
from utils import (
    get_embedding,
    caculate_sentence_similarity
)
QUERY_1 = "Bạn cần kích hoạt JavaScript để chạy ứng dụng này."
QUERY_2 = "You need to enable JavaScript to run this app."

embedding_query_1 = get_embedding(query=QUERY_1)
embedding_query_2 = get_embedding(query=QUERY_2)
similar_result = caculate_sentence_similarity(vector_1=embedding_query_1, vector_2=embedding_query_2)
print(similar_result) ### result = 0.6888
