from fastapi import FastAPI
from app.routers import sentiment

app = FastAPI(title="Sentiment Analysis API")

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(sentiment.router, prefix="/api/v1")


