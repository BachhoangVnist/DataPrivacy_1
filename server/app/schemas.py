from pydantic import BaseModel


class QuestionAnswer(BaseModel):
    question: str
    # model_name: str = None
    # embedding_model_name: str = None
    # k_nearest: str = None

class InferencePolicy(BaseModel):
    url: str
    # model_name: str = None
    # embedding_model_name: str = None
    # k_nearest_legal: str = None
    # k_nearest_policy: str = None
