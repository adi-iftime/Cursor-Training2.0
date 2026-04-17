"""Load sample CSV, add a computed column, save or return rows."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_sample(csv_path: str | Path) -> pd.DataFrame:
    """Load rows from a CSV file (expects at least id, value columns)."""
    return pd.read_csv(csv_path)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with value_doubled = 2 * value."""
    out = df.copy()
    out["value_doubled"] = out["value"] * 2
    return out


def rows_as_records(df: pd.DataFrame) -> list[dict[str, object]]:
    """Return rows as plain dicts (handy for tests / callers without pandas)."""
    return df.to_dict(orient="records")


def save_processed(df: pd.DataFrame, csv_path: str | Path) -> None:
    """Write transformed rows to CSV (no index column)."""
    df.to_csv(csv_path, index=False)


def main() -> None:
    base = Path(__file__).resolve().parent
    source = base / "sample.csv"
    destination = base / "sample_processed.csv"

    loaded = load_sample(source)
    processed = transform(loaded)
    save_processed(processed, destination)
    print(f"Wrote {destination}")
    print(processed.to_string(index=False))


if __name__ == "__main__":
    main()
