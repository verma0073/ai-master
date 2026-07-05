from fastapi import FastAPI

from apps.fastapi_app.app.api.routes import router

app = FastAPI(
    title="AI Master API",
    version="0.1.0",
)

app.include_router(router)
