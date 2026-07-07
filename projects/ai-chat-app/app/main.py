from fastapi import FastAPI

from app.api.route import router as chat_router

from app.core.config import get_settings

settings = get_settings()

print("DEFAULT_PROVIDER FROM SETTINGS:", settings.DEFAULT_PROVIDER)

app = FastAPI(
    title="AI Chat Application",
    version="0.1.0"
)

app.include_router(chat_router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
