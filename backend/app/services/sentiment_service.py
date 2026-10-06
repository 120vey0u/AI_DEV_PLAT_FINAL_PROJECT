from sqlalchemy.orm import Session

from app.ai.gemini_client import analyze_aspects
from app.database import crud


def process_text(db: Session, text: str) -> dict:
    analysis_data = analyze_aspects(text)
    row = crud.create_analysis(db, input_text=text, analysis_data=analysis_data)
    return {
        "id": row.id,
        "input_text": row.input_text,
        "created_at": row.created_at,
        "analysis_data": analysis_data,
    }