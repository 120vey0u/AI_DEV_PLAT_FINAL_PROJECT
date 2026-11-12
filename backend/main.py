from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import sentiment

app = FastAPI(title="Sentiment Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://sentimentanalysis-kappa.vercel.app",
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(sentiment.router, prefix="/api/v1")