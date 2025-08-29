# Import necessary libraries from Flask for web server functionality
# and from Hugging Face Transformers for the AI model.
from flask import Flask, request, jsonify
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Initialize the Flask application.
app = Flask(__name__)

# --- Model and Tokenizer Loading ---
"""
This section is executed only once when the application starts.
Loading the model into memory at startup is a crucial optimization,
as it avoids the high cost of reloading the model on every API request.
"""
model_name = 'gpt2'

print("Loading model...")
model = GPT2LMHeadModel.from_pretrained(model_name)

print("Loading tokenizer...")
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
print("Model and tokenizer loaded successfully.")


@app.route('/generate', methods=['POST'])
def generate_text():
    """
    API endpoint that receives a text prompt and returns a generated text sequence.
    The operational flow is as follows:
    1. RECEIVE PAYLOAD: Extracts the prompt from the incoming JSON.
    2. TOKENIZATION (ENCODING): Converts the text into numerical tokens.
    3. INFERENCE: Generates a new sequence of tokens based on the input.
    4. DECODING: Converts the output tokens back into a human-readable string.
    5. RETURN RESPONSE: Sends the generated text back to the client.
    """
    prompt = request.json.get('prompt')

    if not prompt:
        return jsonify({"error": "Prompt not found in request payload"}), 400

    # `return_tensors="pt"` specifies the output should be a PyTorch tensor.
    inputs = tokenizer.encode(prompt, return_tensors="pt")

    """
    The model.generate() method performs the core inference task.
    - max_length: Limits the total output length to prevent infinite responses.
    - num_return_sequences: Defines how many different completions to generate.
    - no_repeat_ngram_size: Prevents the model from repeating the same sequence
      of 2 words, which improves the quality and coherence of the text.
    """
    outputs = model.generate(inputs, max_length=1000,
                             num_return_sequences=1, no_repeat_ngram_size=2)

    # `skip_special_tokens=True` removes technical tokens (e.g., end-of-sequence)
    # from the final text for a cleaner, human-readable output.
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return jsonify({'response': response})


if __name__ == "__main__":
    """
    This block ensures that the Flask development server runs only when
    the script is executed directly (not when imported as a module).

    In a production environment, debug would be set to False, and a proper
    WSGI server like Gunicorn or uWSGI would be used to run the application.
    """
    app.run(debug=True, host='0.0.0.0', port=5000)
