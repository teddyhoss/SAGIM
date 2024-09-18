from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

REGOLO_API_KEY = os.environ.get('REGOLO_API_KEY')

# Leggi il contesto dal file
with open('context.txt', 'r') as file:
    CONTEXT = file.read().strip()

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    full_prompt = f"{CONTEXT}\n\nUser: {user_input}\nAssistant:"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {REGOLO_API_KEY}"
    }
    
    data = {
        "model": "llama3.1:70b-instruct-q8_0",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": full_prompt}
        ]
    }
    
    response = requests.post('https://api.regolo.ai/v1/chat/completions', 
                             headers=headers, json=data)
    
    if response.status_code == 200:
        return jsonify({"response": response.json()['choices'][0]['message']['content']})
    else:
        return jsonify({"error": "Failed to get response from Regolo.ai"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)