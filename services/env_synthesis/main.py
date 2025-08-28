from fastapi import FastAPI

app = FastAPI(title="env synthesis Service".title())

@app.get("/")
async def root():
    return {"service": "env_synthesis"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
