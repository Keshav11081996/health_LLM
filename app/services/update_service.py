import ast
import json
import re
import os
from app.services.shared import model, tokenizer 

device = "cuda" if os.getenv("USE_CUDA", "true").lower() == "true" else "cpu"

async def analyze_goal_and_suggest_next(last_goal_content: str, completion_rate: float):
    prompt = (
        f"The user completed the goal: '{last_goal_content}' with a completion rate of {completion_rate}%. "
        "Please calculate impact factors which determines how much impact will this have on wellness (it is factor b/w 0 and 0.1), and suggest a new goal "
        "based on the user's progress and context. Respond in the following JSON format, don't include any comment in json:\n"
        "{\n"
        "  \"impact_factors\": {\"Physical Wellness Score\": <float>, \"Mental Wellness Score\": <float>, \"Social Wellness Score\": <float>, \"Sleep Wellness Score\": <float>, \"Nutrition Wellness Score\": <float>},\n"
        "  \"new_goal\": {\"title\": \"<new goal description>\", \"description\": \"<details about the goal>\"}\n"
        "}"
    )

    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    outputs = model.generate(inputs.input_ids, max_new_tokens=300, do_sample=True)
    response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    try:
        json_pattern = re.compile(r'\{(?:[^{}"]|"[^"]*"|\d+\.\d+)*\}', re.DOTALL)
        json_matches = json_pattern.findall(response_text)
        
        impact_factors = json_matches[2]
        new_goal = json_matches[3]
        
    except json.JSONDecodeError:
        raise ValueError("Failed to parse JSON from the model's response.")

    return [ast.literal_eval(impact_factors), ast.literal_eval(new_goal)]

async def update_scores_with_llm(initial_scores: dict, last_goal_content: str, completion_rate: float):
    temp_result = await analyze_goal_and_suggest_next(last_goal_content, completion_rate)
    impact_factors, new_goal = temp_result[0], temp_result[1]
    updated_scores = {}
    
    for key in initial_scores:
        updated_scores[key] = initial_scores[key] + (5 * impact_factors.get(key, 0))
    
    return updated_scores, new_goal