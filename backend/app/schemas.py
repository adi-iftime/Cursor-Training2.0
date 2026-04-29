"""Pydantic schemas shared by routers."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WorkoutCreate(BaseModel):
    title: str
    duration_min: float = 0.0
    calories: float | None = None
    notes: str | None = None
    activity_type_id: int | None = None


class WorkoutOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    duration_min: float
    calories: float | None
    notes: str | None
    activity_type_id: int | None
    performed_at: datetime


class MetricsSummary(BaseModel):
    total_workouts: int
    total_minutes: float
    total_calories: float
    avg_duration_min: float
