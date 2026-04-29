"""Task D1: Load raw workout rows from CSV into SQLite (independent of dimension job)."""
import csv
import sys
from datetime import datetime
from pathlib import Path

# Run from repo root: python -m data.pipeline.ingest_csv
# Or: cd repo && PYTHONPATH=backend python data/pipeline/ingest_csv.py

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from sqlalchemy.orm import Session

from app.db import SessionLocal, engine
from app.models import Base, Workout


def ensure_schema():
    Base.metadata.create_all(bind=engine)


def default_csv_path() -> Path:
    p = ROOT / "data" / "raw" / "workouts_sample.csv"
    if not p.exists():
        p.write_text(
            "title,duration_min,calories,performed_at\n"
            "Morning run,30,220,2025-01-15T08:00:00\n"
            "Yoga,45,120,2025-01-14T18:30:00\n",
            encoding="utf-8",
        )
    return p


def run(path: Path | None = None) -> int:
    ensure_schema()
    csv_path = path or default_csv_path()
    db: Session = SessionLocal()
    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                performed_at = datetime.fromisoformat(row["performed_at"].replace("Z", "+00:00"))
                if performed_at.tzinfo:
                    performed_at = performed_at.replace(tzinfo=None)
                w = Workout(
                    title=row["title"],
                    duration_min=float(row["duration_min"]),
                    calories=float(row["calories"]) if row.get("calories") else None,
                    performed_at=performed_at,
                )
                db.add(w)
        db.commit()
        from sqlalchemy import func, select

        return db.scalar(select(func.count()).select_from(Workout)) or 0
    finally:
        db.close()


if __name__ == "__main__":
    n = run()
    print(f"Ingested rows; total workouts in DB: {n}")
