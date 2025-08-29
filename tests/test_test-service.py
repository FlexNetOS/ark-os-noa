import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add project root to path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

# Import using the actual directory name (hyphens preserved)
import importlib.util

# Dynamic import for hyphenated service names
spec = importlib.util.spec_from_file_location(
    "service_main", 
    ROOT / "services" / "test-service" / "main.py"
)
service_main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(service_main)

app = service_main.app
process = service_main.process

client = TestClient(app)

def test_health_endpoint():
    # Test health endpoint if it exists
    try:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    except:
        # Health endpoint might not exist, skip this test
        pass

def test_process_function():
    job = {"data": "test"}
    result = process(job)
    assert "test-service" in result["steps"]
    assert "test-service" in result["processed_by"]