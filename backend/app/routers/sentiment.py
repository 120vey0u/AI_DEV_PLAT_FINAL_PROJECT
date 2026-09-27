from fastapi import APIRouter
from app.schemas import AnalyzeRequest, AnalyzeResponse

router = APIRouter()

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_text(body: AnalyzeRequest):
    return AnalyzeResponse(
        id=1,
        text=body.text,
        label="positive",
        score=0.95
    )