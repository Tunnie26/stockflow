from fastapi import FastAPI

from app.api.v1.router import router as v1_router

app = FastAPI(title="StockFlow API", version="0.1.0")


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(v1_router, prefix="/api/v1")
