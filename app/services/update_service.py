import ast
import json
import re
import os
from app.services.shared import model, tokenizer


async def extract_between_markers(input_string):
    start_marker = '}.<|eot_id|><|start_header_id|>assistant<|end_header_id|>'
    end_marker = '}<|eot_id|>'
    
    start_index = input_string.find(start_marker)
    end_index = input_string.find(end_marker, start_index)
    
    print(start_index, end_index)
    
    if start_index != -1 and end_index != -1:
        start_index += len(start_marker)
        extracted_data = input_string[start_index:end_index].strip()
        return extracted_data
    else:
        return None  

async def analyze_goal_and_suggest_next(last_goal_content: str, completion_rate: float):
    messages = [
        {
            "role": "user",
            "content": f"I have completed the goal: '{last_goal_content}' with a completion rate of {completion_rate}%."
        },
        {
            "role": "assistant",
            "content": "I am your health assistant, how can I help you?"
        },
        {
            "role": "user",
            "content": f"""Based on this progress and context, please calculate the value of impact factors which determines how much impact this will have on wellness (it is a factor between 0 and 0.1) and strictly respond in the below JSON style, no extra information - 
            {{
                "impact_factors": {{
                    "physical_wellness_score": <float>, 
                    "mental_wellness_score": <float>, 
                    "social_wellness_score": <float>, 
                    "sleep_wellness_score": <float>, 
                    "nutrition_wellness_score": <float>
                }},
                "new_goal": {{
                    "title": "<new goal description>", 
                    "description": "<details about the goal>"
                }}
            }}."""
        }
    ]

    model_inputs = tokenizer.apply_chat_template(messages, return_tensors="pt")
    generated_ids = model.generate(model_inputs, max_new_tokens=300, do_sample=True)
    decoded = tokenizer.batch_decode(generated_ids)
    response_text = decoded[0]
    
    result = await extract_between_markers(response_text)
    # try:
    data_dict = json.loads(result+'}')
    print(data_dict)
    # except json.JSONDecodeError as e:
    #     print(f"JSON Decode Error: {e}")
    #     return None, None  
    
    return [data_dict['impact_factors'], data_dict['new_goal']]

async def update_scores_with_llm(initial_scores: dict, last_goal_content: str, completion_rate: float):
    temp_result = await analyze_goal_and_suggest_next(last_goal_content, completion_rate)
    impact_factors, new_goal = temp_result[0], temp_result[1]
    
    updated_scores = {}
    for key in initial_scores:
        print(initial_scores[key] , 5 * impact_factors.get(key, 0))
        updated_scores[key] = initial_scores[key] + (5 * impact_factors.get(key, 0))
    
    return updated_scores, new_goal
