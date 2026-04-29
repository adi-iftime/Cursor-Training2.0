"""ORM models (scaffold)."""
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class ActivityType(Base):
    __tablename__ = "activity_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    label: Mapped[str] = mapped_column(String(128))

    workouts: Mapped[list["Workout"]] = relationship(back_populates="activity_type")


class Workout(Base):
    __tablename__ = "workouts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    activity_type_id: Mapped[int | None] = mapped_column(ForeignKey("activity_types.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(256))
    duration_min: Mapped[float] = mapped_column(Float, default=0.0)
    calories: Mapped[float | None] = mapped_column(Float, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    performed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    activity_type: Mapped["ActivityType | None"] = relationship(back_populates="workouts")


class DailyRollup(Base):
    __tablename__ = "daily_rollups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    day: Mapped[date] = mapped_column(Date, index=True)
    total_minutes: Mapped[float] = mapped_column(Float, default=0.0)
    total_calories: Mapped[float] = mapped_column(Float, default=0.0)
    workout_count: Mapped[int] = mapped_column(Integer, default=0)
