from fastapi import APIRouter
from server.app import schemas
from inference_privacy_policy import main as inference_policy
from inference_question_answer import main as inference_question

router = APIRouter(
    prefix="/llm",
    tags=["LLMs"]
)

@router.post("/question_answer")
def get_question_answer(request: schemas.QuestionAnswer):
    output = inference_question(question=request.question)
    return output


@router.post("/policy")
def get_inference_policy(request: schemas.InferencePolicy):
    output = inference_policy(url_path=request.url)
    return output
