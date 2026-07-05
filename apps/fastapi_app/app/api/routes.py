
from fastapi import APIRouter

from apps.fastapi_app.app.schemas.chat import ChatRequest, ChatResponse
from apps.fastapi_app.app.services.chat_service import ChatService

router = APIRouter()

chat_service = ChatService()


@router.get("/")
def root():
    return {"message": "AI Master API is running"}


@router.get("/health")
def health():
    return {"status": "healthy"}


@router.post("/v1/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = chat_service.generate_response(request.message)

    return ChatResponse(response=response)
