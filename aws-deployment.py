import boto3
import json
from transformers import GPT2LMHeadModel, GPT2Tokenizer

s3_client = boto3.client('s3')
lambda_client = boto.client('lambda')

# --- Model and Tokenizer Loading ---
# Note: For production Lambda, this loading should happen outside the handler
# to leverage execution context reuse and avoid reloading on every warm invocation.
model_name = 'gpt2'
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Lambda handler function to generate text


def lambda_handler(event, context):
    """
    AWS Lambda handler to generate text using the GPT-2 model.
    Expects an event object containing a 'prompt' key.
    """
    prompt = event['prompt']
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=1000,
                             num_return_sequences=1, no_repeat_ngram_size=2)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return {
        'statusCode': 200,
        'body': json.dumps({'response': response})
    }
