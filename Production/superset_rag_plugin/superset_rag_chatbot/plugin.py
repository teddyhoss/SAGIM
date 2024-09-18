import os
import requests
from flask import request, jsonify
from flask_appbuilder import expose
from superset.views.base import BaseSupersetView
from superset import db
from sqlalchemy import text

REGOLO_TOKEN = os.environ.get('REGOLO_TOKEN')
REGOLO_EMBEDDING_URL = "https://api.regolo.ai/v1/embeddings"
REGOLO_CHAT_URL = "https://api.regolo.ai/v1/chat/completions"

class ChatbotViz:
    viz_type = "chatbot"
    verbose_name = "Chatbot"
    is_timeseries = False
    credits = 'a custom viz plugin'
    
    def get_js_files(self):
        return ['chatbot.js']
    
    def get_css_files(self):
        return []
    
class RAGChatbotView(BaseSupersetView):
    route_base = "/rag-chatbot"

    def get_embedding(self, text):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {REGOLO_TOKEN}"
        }
        data = {
            "input": text,
            "model": "Alibaba-NLP/gte-Qwen2-7B-instruct"
        }
        response = requests.post(REGOLO_EMBEDDING_URL, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['data'][0]['embedding']
        else:
            raise Exception(f"Error getting embedding: {response.text}")

    def get_relevant_data(self, query):
        # Esempio semplificato: recupera dati dalla tabella 'market_predictions'
        # In un'implementazione reale, dovresti usare l'embedding per trovare dati rilevanti
        sql = text("SELECT * FROM market_predictions LIMIT 5")
        with db.engine.connect() as connection:
            result = connection.execute(sql)
            return [dict(row) for row in result]

    def get_chat_completion(self, messages):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {REGOLO_TOKEN}"
        }
        data = {
            "model": "llama3.1:70b-instruct-q8_0",
            "messages": messages
        }
        response = requests.post(REGOLO_CHAT_URL, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            raise Exception(f"Error getting chat completion: {response.text}")

    @expose('/query', methods=['POST'])
    def query(self):
        try:
            user_input = request.json.get('query')
            
            # Genera embedding per la query dell'utente
            user_embedding = self.get_embedding(user_input)
            
            # Recupera dati rilevanti
            relevant_data = self.get_relevant_data(user_input)
            
            # Prepara il contesto per il modello di linguaggio
            context = "\n".join([str(data) for data in relevant_data])
            
            # Prepara i messaggi per il modello di chat
            messages = [
                {"role": "system", "content": "You are a helpful assistant with access to market prediction data."},
                {"role": "user", "content": f"Query: {user_input}\nContext: {context}"}
            ]
            
            # Ottiene una risposta dal modello di chat
            response = self.get_chat_completion(messages)
            
            return jsonify({"response": response})
        except Exception as e:
            return jsonify({"error": str(e)}), 500