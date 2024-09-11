import numpy as np
import os

from app.models.wellness_models import (
    PhysicalWellnessInput,
    MentalWellnessInput,
    SocialWellnessInput,
    SleepWellnessInput,
    NutritionWellnessInput
)

def normalize_metric(actual, max_value):
    return min((actual / max_value) * 100, 100)

def calculate_weighted_score(metrics, weights):
    normalized_metrics = np.array(metrics)
    weighted_score = np.dot(normalized_metrics, weights)
    return weighted_score

def calculate_physical_wellness(input: PhysicalWellnessInput):
    normalized_steps = normalize_metric(input.steps, 10000)
    normalized_exercise_frequency = normalize_metric(input.exercise_frequency, 7)
    normalized_hrv = input.hrv
    
    metrics = [normalized_steps, normalized_exercise_frequency, normalized_hrv]
    weights = [0.3, 0.4, 0.3]
    
    return calculate_weighted_score(metrics, weights)

def calculate_mental_wellness(input: MentalWellnessInput):
    normalized_mood = normalize_metric(input.mood, 10)
    normalized_stress_levels = input.stress_levels
    normalized_meditation_frequency = normalize_metric(input.meditation_frequency, 7)

    metrics = [normalized_mood, normalized_stress_levels, normalized_meditation_frequency]
    weights = [0.4, 0.3, 0.3]
    
    return calculate_weighted_score(metrics, weights)

def calculate_social_wellness(input: SocialWellnessInput):
    normalized_social_interactions = input.social_interactions
    normalized_quality_of_interactions = normalize_metric(input.quality_of_interactions, 10)

    metrics = [normalized_social_interactions, normalized_quality_of_interactions]
    weights = [0.5, 0.5]
    
    return calculate_weighted_score(metrics, weights)

def calculate_sleep_wellness(input: SleepWellnessInput):
    normalized_sleep_duration = normalize_metric(input.sleep_duration, 8)
    normalized_sleep_quality = input.sleep_quality
    
    metrics = [normalized_sleep_duration, normalized_sleep_quality]
    weights = [0.5, 0.5]
    
    return calculate_weighted_score(metrics, weights)

def calculate_nutrition_wellness(input: NutritionWellnessInput):
    normalized_diet_quality = input.diet_quality
    normalized_hydration_levels = normalize_metric(input.hydration_levels, 100)

    metrics = [normalized_diet_quality, normalized_hydration_levels]
    weights = [0.6, 0.4]
    
    return calculate_weighted_score(metrics, weights)

def calculate_holistic_wellness(physical, mental, social, sleep, nutrition, primary_goal):
    metrics = [physical, mental, social, sleep, nutrition]
    base_weights = [0.3, 0.2, 0.2, 0.2, 0.1]
    
    goal_weight_map = {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3,
        "E": 4
    }
    
    goal_index = goal_weight_map.get(primary_goal)
    if goal_index is not None:
        base_weights[goal_index] += 0.1
        total_weight = sum(base_weights)
        weights = [w / total_weight for w in base_weights]
    else:
        weights = base_weights
    
    return calculate_weighted_score(metrics, weights)
