from flask import Flask, request, jsonify, render_template
import sqlite3
import requests
import os
import logging
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

app = Flask(__name__)

REGOLO_TOKEN = os.getenv('REGOLO_TOKEN')
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'

logging.basicConfig(level=logging.DEBUG if DEBUG_MODE else logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    conn = sqlite3.connect('export_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS responses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  question TEXT,
                  user_response TEXT,
                  llm_analysis TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Dizionario per i prompt personalizzati
custom_prompts = {
    "Come si chiama la tua azienda?": "Analizza il nome dell'azienda. Ci sono particolarità o significati nascosti? Suggerisci come questo nome potrebbe essere percepito in mercati internazionali.",
    "Quale la tua Ragione Sociale (P.IVA)?": "Verifica il formato della P.IVA. È coerente con gli standard italiani? Fornisci informazioni sulla struttura aziendale che si può dedurre.",
    "In che settore operi?": "Analizza il settore indicato. Quali sono le tendenze attuali in questo settore a livello internazionale? Suggerisci potenziali mercati esteri interessanti.",
    "Da quanti anni è aperta e attiva la azienda?": "Considera l'età dell'azienda. Quali sfide e opportunità potrebbe affrontare nell'espansione internazionale basandosi sulla sua esperienza?",
    "Su quali piattaforme social media è attualmente presente la vostra azienda?": "Valuta la presenza sui social media. Sono adeguate per i mercati internazionali? Suggerisci strategie per ottimizzare la presenza social per l'espansione all'estero.",
    "Avete già condotto campagne di marketing sui social media per mercati internazionali? Se sì, quali?": "Analizza l'esperienza in campagne internazionali. Quali lezioni si possono trarre? Suggerisci miglioramenti o nuove strategie basate su best practices internazionali.",
    "Quali sono le vostre maggiori preoccupazioni riguardo l'esportazione in nuovi mercati?": "Esamina le preoccupazioni espresse. Sono comuni per aziende simili? Fornisci consigli su come affrontare queste sfide e minimizzare i rischi.",
    "Quale prodotto e/o prodotti vorresti esportare?": "Analizza i prodotti menzionati. Sono adatti per l'esportazione? Suggerisci modifiche o adattamenti per renderli più appetibili in mercati internazionali.",
    "Vuoi spostare la produzione all'estero?": "Considera i pro e i contro dello spostamento della produzione all'estero basandoti sulla risposta. Fornisci consigli su potenziali location e strategie di implementazione.",
    "Vuoi trovare nuovi fornitori per il tuo mercato?": "Analizza la risposta riguardo i nuovi fornitori. Suggerisci strategie per la ricerca di fornitori affidabili in mercati internazionali e considera i rischi e le opportunità."
}

def analyze_with_llm(question, user_response):
    custom_prompt = custom_prompts.get(question, "Analizza la risposta nel contesto dell'esportazione e del commercio internazionale.")
    prompt = f"Analizza la seguente risposta alla domanda '{question}': '{user_response}'. {custom_prompt}"
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {REGOLO_TOKEN}'
    }
    data = {
        "model": "llama3.1:70b-instruct-q8_0",
        "messages": [
            {"role": "system", "content": "Sei un assistente esperto in commercio internazionale e analisi di business."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post('https://api.regolo.ai/v1/chat/completions', json=data, headers=headers)
    llm_response = response.json()['choices'][0]['message']['content']
    return llm_response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_single', methods=['POST'])
def submit_single():
    data = request.json
    question = data['question']
    user_response = data['response']

    llm_analysis = analyze_with_llm(question, user_response)

    if DEBUG_MODE:
        logger.debug(f"Domanda: {question}")
        logger.debug(f"Risposta utente: {user_response}")
        logger.debug(f"Analisi LLM: {llm_analysis}")
        return jsonify({
            "success": True, 
            "message": "Dati elaborati in modalità debug",
            "debug_info": {
                "question": question,
                "user_response": user_response,
                "llm_analysis": llm_analysis
            }
        })
    else:
        conn = sqlite3.connect('export_data.db')
        c = conn.cursor()
        c.execute("INSERT INTO responses (question, user_response, llm_analysis) VALUES (?, ?, ?)",
                  (question, user_response, llm_analysis))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Risposta analizzata e salvata con successo"})

@app.route('/get_data', methods=['GET'])
def get_data():
    conn = sqlite3.connect('export_data.db')
    c = conn.cursor()
    
    c.execute("SELECT question, user_response, llm_analysis FROM responses")
    
    data = c.fetchall()
    conn.close()
    
    formatted_data = [{"question": row[0], "user_response": row[1], "llm_analysis": row[2]} for row in data]
    
    return jsonify(formatted_data)

if __name__ == '__main__':
    app.run(debug=DEBUG_MODE)