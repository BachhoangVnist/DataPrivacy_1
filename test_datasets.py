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

# Test similarity vector base module
from configs import EMBEDDING_MODEL_PATH
from embeddings import EmbeddingModel
from evaluator import VectorBaseEvaluator
embedding_model = EmbeddingModel(model_name=EMBEDDING_MODEL_PATH)
vector_base_evaluator = VectorBaseEvaluator(embedding_model=embedding_model)
vector_base_evaluator.evaluate_csv(input_path="evaluator/test_set.csv", output_file="evaluator/test_result.csv")
