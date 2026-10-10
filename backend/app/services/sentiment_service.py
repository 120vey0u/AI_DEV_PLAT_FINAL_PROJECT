from sqlalchemy.orm import Session
<<<<<<< HEAD
from app.ai.huggingface_client import analyze_sentiment
=======

from app.ai.gemini_client import analyze_aspects
>>>>>>> c2e91e31c7c9260c66836d7204f61c33b539f3cd
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