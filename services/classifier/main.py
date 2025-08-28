from fastapi import FastAPI

app = FastAPI(title="classifier Service".title())

@app.get("/")
async def root():
    return {"service": "classifier"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
