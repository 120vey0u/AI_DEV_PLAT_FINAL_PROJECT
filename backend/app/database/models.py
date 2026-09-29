from sqlalchemy import Column, Integer, String, Text, DateTime, func

from app.database.session import Base


class SentimentHistory(Base):
    __tablename__ = "sentiment_history"

    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(Text, nullable=False)
    sentiment_result = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())