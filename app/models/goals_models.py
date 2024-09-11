from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    role: str
    content: str

class HealthStateRequest(BaseModel):
    messages: List[Message]
