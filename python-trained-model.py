from flask import Flask, request, jsonify
from transformers import GPT2LMHeadModel, GPT2Tokenizer

app = Flask(__name__)

# Carregar o modelo treinado
model_name = 'gpt2'
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

@app.route('/generate', methods=['POST'])
def generate_text():
    prompt = request.json.get('prompt')
    inputs = tokenizer.encode(prompt, return_tensors=""pt"")
    outputs = model.generate(inputs, max_length=1000, num_return_sequences=1, no_repeat_ngram_size=2)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return jsonify({'response': response})

if __name__ == ""__main__"":
    app.run(debug=True)
