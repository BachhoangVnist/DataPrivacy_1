LOCAL_VECTOR_PATH = "vectorstores/db_faiss"
LOCAL_GENERATOR_PDF_FOLDER = "pdf"
EMBEDDING_MODEL_PATH = "bkai-foundation-models/vietnamese-bi-encoder"
LLM_MODEL_PATH = "models/vinallama-7b-chat_q5_0.gguf"
LLM_MODEL_HUB = "LR-AI-Labs/vbd-llama2-7B-50b-chat"
DEFAULT_EVALUATOR_OUTPUT_PATH = "evaluator/test_result.csv"
DEFAULT_EVALUATOR_INPUT_PATH = "evaluator/test_set.csv"
DEFAULT_PROMPT_TEMPLATE = (
    "<|im_start|>system\nSử dụng thông tin sau đây để trả lời câu hỏi. "
    "Nếu bạn không biết câu trả lời, hãy nói không biết, đừng cố tạo ra câu trả lời\n\n"
    "        {context}<|im_end|>\n<|im_start|>user\n{question}"
    "<|im_end|>\n<|im_start|>assistant"
)
COOKIE_REFERENCE_PROMPT_TEMPLATE = (
    "<|im_start|>system\nSử dụng thông tin sau đây để trả lời câu hỏi. "
    "Nếu bạn không biết câu trả lời, hãy nói không biết, đừng cố tạo ra câu trả lời\n\n"
    "        {context}<|im_end|>\n<|im_start|>user\n"
    "xem xét văn bản chính sách bảo mật sau đây có tiềm ẩn rủi ro gì đỗi với quyền "
    "riêng tư của người dùng hay không\n{question}"
    "<|im_end|>\n<|im_start|>assistant"
)
COOKIE_QUESTION_TEMPLATE = (
    "Có những nguy cơ về quyền riêng tư của người dùng liên quan đến việc "
    "sử dụng cookie trong nội dung của chính sách bảo mật này không:\n\n"
    "{content}"
)
DEFAULT_COOKIE_POLICY_QUERY = "quyền riêng tư và vấn đề liên quan đến cookie"
LLAMA2_INFERENCEE_PROMPT_TEMPLATE = (
    "<s>[INST] <<SYS>> system: Sử dụng thông tin sau đây để trả lời câu hỏi. Nếu bạn "
    "không biết câu trả lời, hãy nói không biết, đừng cố tạo ra câu trả lời\n<</SYS>>"
    " context: {context}\n\nuser: "
    "xem xét văn bản chính sách bảo mật sau đây có tiềm ẩn rủi ro gì đỗi với quyền "
    "riêng tư của người dùng hay không\n{question}"
    " [/INST]"
)
QLORA_INFERENCEE_PROMPT_TEMPLATE = (
    "system: Sử dụng thông tin sau đây để trả lời câu hỏi. "
    "Nếu bạn không biết câu trả lời, hãy nói không biết, đừng cố tạo ra câu trả lời"
    "\n\ncontext: {context}\n\nuser: "
    "xem xét văn bản chính sách bảo mật sau đây có tiềm ẩn rủi ro gì đỗi với quyền "
    "riêng tư của người dùng hay không\n{question}"
    "\n\nassistant:"
)
QLORA_QA_PROMPT_TEMPLATE = (
    "system: Sử dụng thông tin sau đây để trả lời câu hỏi. "
    "Nếu bạn không biết câu trả lời, hãy nói không biết, đừng cố tạo ra câu trả lời"
    "\n\ncontext: {context}"
    "\n\nuser: {question}"
    "\n\nassistant:"
)
