import os
import re
import json
from fastapi import HTTPException
from transformers import AutoModelForCausalLM, AutoTokenizer
from app.models.goals_models import HealthStateRequest
import asyncio
from app.services.shared import model, tokenizer  

device = "cuda" if os.getenv("USE_CUDA", "true").lower() == "true" else "cpu"

async def generate_goals(request: HealthStateRequest):
    messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
    messages[-1]["content"] += "\nPlease provide the output strictly in JSON format with keys 'goals' containing a list of goals with their descriptions."

    encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")
    model_inputs = encodeds.to(device)
    model.to(device)

    generated_ids = model.generate(model_inputs, max_new_tokens=300, do_sample=True)
    decoded = tokenizer.batch_decode(generated_ids)

    response_text = decoded[0]
    cleaned_response = re.sub(r"<s>|</s>|\[INST\]|\[/INST\]", "", response_text).strip()

    try:
        json_parts = re.findall(r'\{[^{}]*\}', cleaned_response, re.DOTALL)
        json_parts = [part.replace("\n", "").strip() for part in json_parts]

        parsed_dicts = []
        for part in json_parts:
            parsed_dict = json.loads(part)
            parsed_dicts.append(parsed_dict)
            
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse JSON from the model's response.")

    return {"goals": parsed_dicts[-2:]}