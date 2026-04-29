"""Task B2: Metrics REST router."""
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import DailyRollup, Workout
from app.schemas import MetricsSummary

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/kpi")
def kpi_snapshot(db: Session = Depends(get_db)):
    """Dashboard KPI bundle (mirrors analytics/kpi.py logic)."""
    n_workouts = db.scalar(select(func.count()).select_from(Workout)) or 0
    last7 = db.scalars(select(DailyRollup).order_by(DailyRollup.day.desc()).limit(7)).all()
    total_cal_week = sum(r.total_calories for r in last7)
    return {
        "workout_count": int(n_workouts),
        "rollup_days_available": len(last7),
        "last_7d_total_calories": float(total_cal_week),
        "headline": "Stay consistent — small sessions compound.",
    }


@router.get("/summary", response_model=MetricsSummary)
def summary(db: Session = Depends(get_db)):
    total_workouts = db.scalar(select(func.count()).select_from(Workout)) or 0
    agg = db.execute(
        select(
            func.coalesce(func.sum(Workout.duration_min), 0.0),
            func.coalesce(func.sum(Workout.calories), 0.0),
        )
    ).one()
    total_minutes = float(agg[0] or 0)
    total_calories = float(agg[1] or 0)
    avg_duration = total_minutes / total_workouts if total_workouts else 0.0
    return MetricsSummary(
        total_workouts=int(total_workouts),
        total_minutes=total_minutes,
        total_calories=total_calories,
        avg_duration_min=avg_duration,
    )


@router.get("/daily", response_model=list[dict])
def daily_rollups(db: Session = Depends(get_db)):
    rows = db.scalars(select(DailyRollup).order_by(DailyRollup.day.desc()).limit(30)).all()
    return [
        {
            "day": r.day.isoformat(),
            "total_minutes": r.total_minutes,
            "total_calories": r.total_calories,
            "workout_count": r.workout_count,
        }
        for r in rows
    ]
