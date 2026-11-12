from sqlalchemy import Column, Integer, Text, DateTime, JSON, func

from app.database.session import Base


class SentimentHistory(Base):
    __tablename__ = "sentiment_history"

    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(Text, nullable=False)
    analysis_data = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())