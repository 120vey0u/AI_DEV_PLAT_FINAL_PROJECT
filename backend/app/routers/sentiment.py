from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.database.session import get_db
from app.services.sentiment_service import process_text

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_text(body: AnalyzeRequest, db: Session = Depends(get_db)):
    result = process_text(db, body.text)
    return AnalyzeResponse(**result)