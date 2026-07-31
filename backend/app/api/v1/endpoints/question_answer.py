from fastapi import APIRouter

from app.schemas.question_answer import AskRequest, AskResponse
from app.services.question_answer_service import QuestionAnswerService

router = APIRouter()

service = QuestionAnswerService()


@router.post(
    "/ask",
    response_model=AskResponse,
)
def ask_question(request: AskRequest):

    return service.answer_question(
        repository_name=request.repository_name,
        question=request.question,
    )