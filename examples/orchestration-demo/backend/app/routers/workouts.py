"""Task B1: Workouts REST router."""
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Workout
from app.schemas import WorkoutCreate, WorkoutOut

router = APIRouter(prefix="/workouts", tags=["workouts"])


@router.get("", response_model=list[WorkoutOut])
def list_workouts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rows = db.scalars(select(Workout).order_by(Workout.performed_at.desc()).offset(skip).limit(limit)).all()
    return rows


@router.post("", response_model=WorkoutOut, status_code=201)
def create_workout(body: WorkoutCreate, db: Session = Depends(get_db)):
    w = Workout(
        title=body.title,
        duration_min=body.duration_min,
        calories=body.calories,
        notes=body.notes,
        activity_type_id=body.activity_type_id,
    )
    db.add(w)
    db.commit()
    db.refresh(w)
    return w


@router.get("/{workout_id}", response_model=WorkoutOut)
def get_workout(workout_id: int, db: Session = Depends(get_db)):
    w = db.get(Workout, workout_id)
    if not w:
        raise HTTPException(status_code=404, detail="Workout not found")
    return w


@router.delete("/{workout_id}", status_code=204)
def delete_workout(workout_id: int, db: Session = Depends(get_db)):
    w = db.get(Workout, workout_id)
    if not w:
        raise HTTPException(status_code=404, detail="Workout not found")
    db.delete(w)
    db.commit()
    return Response(status_code=204)
