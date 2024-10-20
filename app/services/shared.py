import os
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("unsloth/Llama-3.2-3B-Instruct")
model = AutoModelForCausalLM.from_pretrained("unsloth/Llama-3.2-3B-Instruct")