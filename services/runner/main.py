from fastapi import FastAPI

app = FastAPI(title="runner Service".title())

@app.get("/")
async def root():
    return {"service": "runner"}


def process(job: dict) -> dict:
    """Append this service's name to the job step trace."""
    job.setdefault("steps", []).append("runner")
    return job

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
