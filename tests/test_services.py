import sys
from importlib import import_module
from pathlib import Path
from fastapi.testclient import TestClient

# Ensure project root is on the path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

SERVICE_MODULES = [
    "services.intake.main",
    "services.classifier.main",
    "services.graph_extract.main",
    "services.embeddings.main",
    "services.env_synthesis.main",
    "services.safety.main",
    "services.runner.main",
    "services.integrator.main",
    "services.registrar.main",
]


def test_root_endpoints():
    for module_name in SERVICE_MODULES:
        module = import_module(module_name)
        client = TestClient(module.app)
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["service"] == module_name.split(".")[-2]
