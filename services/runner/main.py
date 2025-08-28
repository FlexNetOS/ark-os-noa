from fastapi import FastAPI

app = FastAPI(title="runner Service".title())

@app.get("/")
async def root():
    return {"service": "runner"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
