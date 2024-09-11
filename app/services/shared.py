import os
from transformers import AutoModelForCausalLM, AutoTokenizer

token = os.getenv("HF_TOKEN")
device = "cuda" if os.getenv("USE_CUDA", "true").lower() == "true" else "cpu"
model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2").to(device)
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
