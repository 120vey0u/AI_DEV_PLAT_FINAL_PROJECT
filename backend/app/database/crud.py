from sqlalchemy.orm import Session

from app.database.models import SentimentHistory


def create_analysis(db: Session, input_text: str, analysis_data: dict) -> SentimentHistory:
    obj = SentimentHistory(input_text=input_text, analysis_data=analysis_data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_analysis(db: Session, analysis_id: int) -> SentimentHistory | None:
    return db.query(SentimentHistory).filter(SentimentHistory.id == analysis_id).first()


def list_analyses(db: Session, limit: int = 20, offset: int = 0) -> list[SentimentHistory]:
    return (
        db.query(SentimentHistory)
        .order_by(SentimentHistory.id.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )