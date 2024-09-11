from fastapi import APIRouter
from app.models.update_score_models import UpdateScoreInput
from app.services.update_service import update_scores_with_llm  # Ensure this function is properly defined

router = APIRouter()

@router.post("/update_scores")
async def update_scores_endpoint(input: UpdateScoreInput):
    updated_scores, new_goal = await update_scores_with_llm(
        input.initial_scores, 
        input.last_goal_content, 
        input.completion_rate
    )
    return {"updated_scores": updated_scores, "new_goal": new_goal}