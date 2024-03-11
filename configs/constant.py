LOCAL_VECTOR_PATH = "vectorstores/db_faiss"
LOCAL_GENERATOR_PDF_FOLDER = "pdf"
EMBEDDING_MODEL_PATH = "bkai-foundation-models/vietnamese-bi-encoder"
LLM_MODEL_PATH = "models/vinallama-7b-chat_q5_0.gguf"
LLM_MODEL_HUB = "bachngo/vinallama-7b-chat-gguf"
# DEFAULT_PROMPT_TEMPLATE = """<|im_start|>system\nSử dụng thông tin sau đây để trả lời câu hỏi. Nếu bạn không biết câu trả lời, hãy nói không biết, đừng cố tạo ra câu trả lời\n
#         {context}<|im_end|>\n<|im_start|>user\n{question}<|im_end|>\n<|im_start|>assistant"""
DEFAULT_PROMPT_TEMPLATE = (
    "<|im_start|>system\nSử dụng thông tin sau đây để trả lời câu hỏi. "
    "Nếu bạn không biết câu trả lời, hãy nói không biết, đừng cố tạo ra câu trả lời\n\n"
    "        {context}<|im_end|>\n<|im_start|>user\n{question}"
    "<|im_end|>\n<|im_start|>assistant"
)
