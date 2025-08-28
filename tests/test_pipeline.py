import sys
from pathlib import Path

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
    assert result["steps"] == EXPECTED_STEPS
