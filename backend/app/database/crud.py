from sqlalchemy.orm import Session

from app.database.models import SentimentHistory


def create_history(db: Session, input_text: str, sentiment_result: str) -> SentimentHistory:
    obj = SentimentHistory(input_text=input_text, sentiment_result=sentiment_result)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_history(db: Session, history_id: int) -> SentimentHistory | None:
    return db.query(SentimentHistory).filter(SentimentHistory.id == history_id).first()


def list_history(db: Session, limit: int = 20, offset: int = 0) -> list[SentimentHistory]:
    return (
        db.query(SentimentHistory)
        .order_by(SentimentHistory.id.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )  