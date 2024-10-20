import os
import re
import json
from fastapi import HTTPException
from transformers import AutoModelForCausalLM, AutoTokenizer
from app.models.goals_models import HealthStateRequest
import asyncio
from app.services.shared import model, tokenizer  

async def generate_goals(request: HealthStateRequest):
    messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
    messages[-1]["content"] += "\nPlease provide the output strictly in JSON format with keys 'goals' containing a list of goals with their descriptions."

    model_inputs = tokenizer.apply_chat_template(messages, return_tensors="pt")

    generated_ids = model.generate(model_inputs, max_new_tokens=300, do_sample=True)
    decoded = tokenizer.batch_decode(generated_ids)

    response_text = decoded[0]

    json_match = re.search(r'```(.*?)```', response_text, re.DOTALL)

    if json_match:
        json_str = json_match.group(1).strip()
        response_dict = json.loads(json_str)
    else:
        response_dict = {}

    print(response_dict)
    
    return response_dict