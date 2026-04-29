"""Task DS1: Simple calorie estimation model from workout history."""
import json
import pickle
import sys
from pathlib import Path

import numpy as np
from sklearn.linear_model import LinearRegression

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Workout


def train_and_save(out_path: Path | None = None) -> dict:
    out_path = out_path or (ROOT / "ml" / "calorie_model.pkl")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    db: Session = SessionLocal()
    try:
        rows = db.scalars(select(Workout).where(Workout.calories.isnot(None))).all()
        if len(rows) < 2:
            # trivial fallback coefficients
            coef = np.array([[10.0]])
            intercept = 50.0
            meta = {"n_samples": len(rows), "fallback": True}
        else:
            X = np.array([[w.duration_min] for w in rows])
            y = np.array([w.calories or 0.0 for w in rows])
            reg = LinearRegression().fit(X, y)
            coef = reg.coef_.reshape(1, -1)
            intercept = float(reg.intercept_)
            meta = {"n_samples": len(rows), "fallback": False, "r2": float(reg.score(X, y))}
        payload = {"coef": coef.tolist(), "intercept": intercept, "meta": meta}
        with open(out_path, "wb") as f:
            pickle.dump(payload, f)
        with open(out_path.with_suffix(".json"), "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)
        return meta
    finally:
        db.close()


if __name__ == "__main__":
    m = train_and_save()
    print(json.dumps(m, indent=2))
