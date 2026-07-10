from fastapi import APIRouter, HTTPException

from app.core.exceptions import AIServiceError
from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter()

chat_service = ChatService()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    try:
        response = chat_service.generate_response(
            request.message
        )

        return ChatResponse(
            response=response
        )

    except AIServiceError:
        raise HTTPException(
            status_code=503,
            detail="AI service unavailable"
        )
