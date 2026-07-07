from fastapi import APIRouter

from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter()

chat_service = ChatService()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    response = chat_service.generate_response(
        request.message
    )

    return ChatResponse(
        response=response
    )
