from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)
REGOLO_API_KEY = os.getenv('REGOLO_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/context')
def get_context():
    with open('context.txt', 'r') as file:
        context = file.read()
    return context, 200, {'Content-Type': 'text/plain'}

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    with open('context.txt', 'r') as file:
        context = file.read()

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {REGOLO_API_KEY}'
    }

    payload = {
        "model": "llama3.1:70b-instruct-q8_0",
        "messages": [
            {"role": "system", "content": f"You are a helpful assistant. Context: {context}"},
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post('https://api.regolo.ai/v1/chat/completions', 
                             headers=headers, 
                             json=payload)

    if response.status_code == 200:
        result = response.json()
        assistant_message = result['choices'][0]['message']['content']
        return jsonify({"message": assistant_message})
    else:
        return jsonify({"error": "Failed to get response from Regolo AI"}), 500

if __name__ == '__main__':
    app.run(debug=True)