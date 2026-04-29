"""Task A1: KPI helpers and exportable summary for dashboard."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import DailyRollup, Workout


def compute_kpis() -> dict:
    db: Session = SessionLocal()
    try:
        n_workouts = db.scalar(select(func.count()).select_from(Workout)) or 0
        last7 = db.scalars(select(DailyRollup).order_by(DailyRollup.day.desc()).limit(7)).all()
        streak_days = len(last7)
        total_cal_week = sum(r.total_calories for r in last7)
        return {
            "workout_count": int(n_workouts),
            "rollup_days_available": streak_days,
            "last_7d_total_calories": float(total_cal_week),
            "headline": "Stay consistent — small sessions compound.",
        }
    finally:
        db.close()


def export_json(out_path: Path | None = None) -> Path:
    out_path = out_path or (ROOT / "analytics" / "kpi_export.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    data = compute_kpis()
    out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return out_path


if __name__ == "__main__":
    p = export_json()
    print(p.read_text())
