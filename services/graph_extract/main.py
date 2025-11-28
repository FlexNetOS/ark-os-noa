import sys
from pathlib import Path

from fastapi import FastAPI

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from job import Job

app = FastAPI(title="Graph Extract Service")


@app.get("/")
async def root():
    return {"service": "graph_extract"}


def process(job: Job) -> Job:
    """Record the execution of this service on the job."""
    job.record_step("graph_extract")
def process(job: dict) -> dict:
    """Append this service's name to the job step trace."""
    job.setdefault("steps", []).append("graph_extract")
    return job

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
