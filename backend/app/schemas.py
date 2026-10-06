from datetime import datetime
from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    text: str


class HighlightedSegment(BaseModel):
    text: str
    sentiment: str


class Aspect(BaseModel):
    name: str
    score: int
    sentiment: str


class AnalysisData(BaseModel):
    overall: str
    overall_comment: str
    highlightedText: list[HighlightedSegment]
    aspects: list[Aspect]


class AnalyzeResponse(BaseModel):
    id: int
    input_text: str
    created_at: datetime
    analysis_data: AnalysisData