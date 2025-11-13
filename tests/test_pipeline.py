import sys
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from pipeline import run_pipeline

EXPECTED_STEPS = [
    "intake",
    "classifier",
    "graph_extract",
    "embeddings",
    "env_synthesis",
    "safety",
    "runner",
    "integrator",
    "registrar",
]

def test_run_pipeline():
    result = run_pipeline("data")
    try:
        assert result.steps == EXPECTED_STEPS
        for step in EXPECTED_STEPS:
            marker = result.workspace / f"{step}.txt"
            assert marker.exists()
            assert marker.read_text() == step
    finally:
        shutil.rmtree(result.workspace)
    assert result["steps"] == EXPECTED_STEPS
