import json
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Lazy globals
MODEL_NAME = os.getenv("MODEL_NAME", "distilgpt2")
_model = None
_tokenizer = None

def _load():
    global _model, _tokenizer
    if _model is None or _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
        _model.eval()
        torch.set_grad_enabled(False)

def lambda_handler(event, context):
    prompt = (event or {}).get('prompt')
    if not prompt:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'prompt is required'})
        }

    _load()
    inputs = _tokenizer(prompt, return_tensors="pt", truncation=True, max_length=256)
    with torch.no_grad():
        outputs = _model.generate(
            **inputs,
            max_new_tokens=120,
            do_sample=True,
            temperature=0.8,
            top_p=0.95,
            no_repeat_ngram_size=2,
            pad_token_id=_tokenizer.eos_token_id,
        )
    response = _tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {
        'statusCode': 200,
        'body': json.dumps({'response': response})
    }
