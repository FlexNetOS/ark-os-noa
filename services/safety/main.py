from fastapi import FastAPI

app = FastAPI(title="safety Service".title())

@app.get("/")
async def root():
    return {"service": "safety"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
