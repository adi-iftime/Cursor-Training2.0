"""Lightweight pipeline import checks (optional)."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_transform_module_importable():
    sys.path.insert(0, str(ROOT / "backend"))
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "transform_daily", ROOT / "data" / "pipeline" / "transform_daily.py"
    )
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert callable(mod.run)
