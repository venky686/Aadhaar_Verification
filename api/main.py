from fastapi import FastAPI
from api.routes import router
from utils.config import settings
from utils.logger import app_logger

app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    app_logger.info("Starting Aadhaar Verification API...")

@app.get("/")
async def root():
    return {"message": "Aadhaar Verification API is running"}
