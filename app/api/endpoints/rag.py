from fastapi import APIRouter

from app.models.schemas import AskRequest, AskResponse
from app.services.rag_service import answer

router = APIRouter(tags=["RAG"])


@router.post("/ask", response_model=AskResponse, summary="Ответить на вопрос по индексированным документам")
def ask_question(payload: AskRequest):
    return answer(payload.question)
