from pydantic import BaseModel
from typing import List, Dict

class UpdateScoreInput(BaseModel):
    initial_scores: Dict[str, float]  
    last_goal_content: str 
    completion_rate: float 