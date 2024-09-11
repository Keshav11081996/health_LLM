from fastapi import APIRouter
from app.models.wellness_models import WellnessInput
from app.services.wellness_service import (
    calculate_physical_wellness,
    calculate_mental_wellness,
    calculate_social_wellness,
    calculate_sleep_wellness,
    calculate_nutrition_wellness,
    calculate_holistic_wellness
)

router = APIRouter()

@router.post("/calculate_scores")
def calculate_wellness_scores(input: WellnessInput):
    physical_score = calculate_physical_wellness(input.physical)
    mental_score = calculate_mental_wellness(input.mental)
    social_score = calculate_social_wellness(input.social)
    sleep_score = calculate_sleep_wellness(input.sleep)
    nutrition_score = calculate_nutrition_wellness(input.nutrition)

    holistic_wellness_score = calculate_holistic_wellness(
        physical_score, mental_score, social_score, sleep_score, nutrition_score, input.primary_goal
    )

    return {
        "Physical Wellness Score": physical_score,
        "Mental Wellness Score": mental_score,
        "Social Wellness Score": social_score,
        "Sleep Wellness Score": sleep_score,
        "Nutrition Wellness Score": nutrition_score,
        "Holistic Wellness Score": holistic_wellness_score,
    }
