from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import AnalyzeRequest, AnalyzeResponse, DeleteResponse
from app.database.session import get_db
from app.database import crud
from app.services.sentiment_service import process_text

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_text(body: AnalyzeRequest, db: Session = Depends(get_db)):
    result = process_text(db, body.text)
    return AnalyzeResponse(**result)


@router.get("/history", response_model=list[AnalyzeResponse])
def get_history(limit: int = 100000000000000000, offset: int = 0, db: Session = Depends(get_db)):
    rows = crud.list_analyses(db, limit=limit, offset=offset)
    return [
        AnalyzeResponse(
            id=r.id,
            input_text=r.input_text,
            created_at=r.created_at,
            analysis_data=r.analysis_data,
        )
        for r in rows
    ]


@router.get("/history/{history_id}", response_model=AnalyzeResponse)
def get_history_item(history_id: int, db: Session = Depends(get_db)):
    row = crud.get_analysis(db, history_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy bản ghi")
    return AnalyzeResponse(
        id=row.id,
        input_text=row.input_text,
        created_at=row.created_at,
        analysis_data=row.analysis_data,
    )


@router.delete("/history/{history_id}", response_model=DeleteResponse)
def delete_history_item(history_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_analysis(db, history_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Không tìm thấy bản ghi")
    return DeleteResponse(message=f"Đã xoá bản ghi id={history_id}")