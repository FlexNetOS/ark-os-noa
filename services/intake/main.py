from fastapi import FastAPI

app = FastAPI(title="intake Service".title())

@app.get("/")
async def root():
    return {"service": "intake"}


def process(job: dict) -> dict:
    """Append this service's name to the job step trace."""
    job.setdefault("steps", []).append("intake")
    return job

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
