"""Task D2: Reference / activity type dimension tables (independent of raw ingest)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from sqlalchemy.orm import Session

from app.db import SessionLocal, engine
from app.models import ActivityType, Base


def ensure_schema():
    Base.metadata.create_all(bind=engine)


def run() -> int:
    ensure_schema()
    db: Session = SessionLocal()
    try:
        seeds = [
            ("run", "Running"),
            ("bike", "Cycling"),
            ("yoga", "Yoga"),
            ("lift", "Strength"),
        ]
        n = 0
        from sqlalchemy import select

        for code, label in seeds:
            existing = db.scalars(select(ActivityType).where(ActivityType.code == code)).first()
            if existing:
                continue
            db.add(ActivityType(code=code, label=label))
            n += 1
        db.commit()
        return n
    finally:
        db.close()


if __name__ == "__main__":
    added = run()
    print(f"Added {added} activity types")
