"""Task D3: Daily aggregation (depends on D1 + D2 data in DB)."""
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.db import SessionLocal, engine
from app.models import Base, DailyRollup, Workout


def ensure_schema():
    Base.metadata.create_all(bind=engine)


def run() -> int:
    ensure_schema()
    db: Session = SessionLocal()
    try:
        db.execute(delete(DailyRollup))
        db.commit()
        day_key = func.strftime("%Y-%m-%d", Workout.performed_at)
        q = select(
            day_key.label("day"),
            func.sum(Workout.duration_min),
            func.sum(Workout.calories),
            func.count(Workout.id),
        ).group_by(day_key)
        rows = db.execute(q).all()
        n = 0
        for day, total_min, total_cal, cnt in rows:
            if day is None:
                continue
            d = date.fromisoformat(str(day)) if not isinstance(day, date) else day
            db.add(
                DailyRollup(
                    day=d,
                    total_minutes=float(total_min or 0),
                    total_calories=float(total_cal or 0),
                    workout_count=int(cnt or 0),
                )
            )
            n += 1
        db.commit()
        return n
    finally:
        db.close()


if __name__ == "__main__":
    n = run()
    print(f"Wrote {n} daily rollup rows")
