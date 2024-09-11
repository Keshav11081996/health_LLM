from fastapi import FastAPI
from app.routers import wellness, goals, update, health

app = FastAPI()

app.include_router(wellness.router, prefix="/wellness", tags=["Wellness"])
app.include_router(goals.router, prefix="/goals", tags=["Goals"])
app.include_router(update.router, prefix="/wellness", tags=["Wellness"])
app.include_router(health.router, prefix="/health", tags=["Health Check"])

