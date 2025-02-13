from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...fastapi import schemas
from ..database import SessionLocal
from . import crud

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/assessments/", response_model=schemas.AssessmentCreate)
def create_assessment(assessment: schemas.AssessmentCreate, db: Session = Depends(get_db)):
    return crud.create_assessment(db=db, assessment=assessment)

@router.get("/assessments/{assessment_id}")
def read_assessment(assessment_id: int, db: Session = Depends(get_db)):
    assessment = crud.get_assessment(db, assessment_id=assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment