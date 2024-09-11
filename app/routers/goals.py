from fastapi import APIRouter, HTTPException
from app.models.goals_models import HealthStateRequest
from app.services.goals_service import generate_goals

router = APIRouter()

@router.post("/generate")
async def generate_goals_endpoint(request: HealthStateRequest):
    return await generate_goals(request)
