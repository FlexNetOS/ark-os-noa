"""Simple sequential pipeline orchestrator for service stubs."""
from typing import Any, Dict

from services.intake import main as intake
from services.model_selector import main as model_selector
from services.classifier import main as classifier
from services.graph_extract import main as graph_extract
from services.embeddings import main as embeddings
from services.env_synthesis import main as env_synthesis
from services.safety import main as safety
from services.runner import main as runner
from services.integrator import main as integrator
from services.registrar import main as registrar

SERVICE_SEQUENCE = [
    intake,
    model_selector,
    classifier,
    graph_extract,
    embeddings,
    env_synthesis,
    safety,
    runner,
    integrator,
    registrar,
]

def run_pipeline(data: Any) -> Dict[str, Any]:
    """Run the stub pipeline by passing a job through each service."""
    job: Dict[str, Any] = {"data": data, "steps": []}
    for module in SERVICE_SEQUENCE:
        job = module.process(job)
    return job
