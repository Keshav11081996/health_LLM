from pydantic import BaseModel

class PhysicalWellnessInput(BaseModel):
    steps: float
    exercise_frequency: float
    hrv: float

class MentalWellnessInput(BaseModel):
    mood: float
    stress_levels: float
    meditation_frequency: float

class SocialWellnessInput(BaseModel):
    social_interactions: float
    quality_of_interactions: float

class SleepWellnessInput(BaseModel):
    sleep_duration: float
    sleep_quality: float

class NutritionWellnessInput(BaseModel):
    diet_quality: float
    hydration_levels: float

class WellnessInput(BaseModel):
    physical: PhysicalWellnessInput
    mental: MentalWellnessInput
    social: SocialWellnessInput
    sleep: SleepWellnessInput
    nutrition: NutritionWellnessInput
    primary_goal: str
