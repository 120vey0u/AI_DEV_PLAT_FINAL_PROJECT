from sqlalchemy.orm import Session

from app.ai.huggingface_client import analyze_sentiment
from app.database import crud


def process_text(db: Session, text: str) -> dict:
    result = analyze_sentiment(text)
    row = crud.create_history(
        db,
        input_text=text,
        sentiment_result=result["label"],
    )
    return {
        "id": row.id,
        "text": row.input_text,
        "label": row.sentiment_result,
        "score": result["score"],
    }