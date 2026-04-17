from pathlib import Path

import pandas as pd

from data.process import load_sample, transform


def test_transform_adds_value_doubled_in_memory():
    df = pd.DataFrame({"id": [1, 2], "value": [3, 7]})
    out = transform(df)
    assert "value_doubled" in out.columns
    assert out["value_doubled"].tolist() == [6, 14]


def test_transform_sample_csv_matches_expected():
    csv_path = Path(__file__).resolve().parent.parent / "data" / "sample.csv"
    df = load_sample(csv_path)
    out = transform(df)
    expected = (df["value"] * 2).tolist()
    assert out["value_doubled"].tolist() == expected
