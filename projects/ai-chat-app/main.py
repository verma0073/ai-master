from fastapi import FastAPI

app = FastAPI(
    title="AI Chat Application",
    version="0.1.0"
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}
