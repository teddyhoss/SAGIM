from flask import Flask, request, jsonify, render_template, g
import sqlite3
import requests
import os
import logging
from dotenv import load_dotenv
import uuid
import tempfile
from pathlib import Path

# Carica le variabili d'ambiente dal file .env
load_dotenv()

app = Flask(__name__)

REGOLO_TOKEN = os.getenv('REGOLO_TOKEN')
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'

logging.basicConfig(level=logging.DEBUG if DEBUG_MODE else logging.INFO)
logger = logging.getLogger(__name__)

# Genera un percorso unico per il database ad ogni avvio dell'applicazione
DB_PATH = os.path.join(tempfile.gettempdir(), f'export_data_{uuid.uuid4()}.db')

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        init_db(g.db)
    return g.db

def init_db(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS responses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  question TEXT,
                  user_response TEXT,
                  llm_analysis TEXT)''')
    conn.commit()

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

def get_db_uuid():
    return Path(DB_PATH).stem.split('_')[-1]

# Dizionario per i prompt personalizzati
custom_prompts = {
    "Come si chiama la tua azienda?": "Analizza il nome dell'azienda. Restutisci il nome della azienda, solamente il nome dell azienda nessuna parola extra, se non rilevi un nome azienda restituisci NO in maiuscolo cosi come ho scritto io ",
    "Quale la tua Ragione Sociale (P.IVA)?": "Verifica il formato della P.IVA. È coerente con gli standard italiani? Se si, Restituisci solamente la PIVA senza nessuna parola extra, se non rilevi una pvia valida restituisci NO in minuscolo cosi come ho scritto io",
    "In che settore operi?": "Analizza il settore indicato e cerca di capire se è in una di queste categorie: Agroalimentare, Moda,Lusso, Meccanica, Design, Arredamento, Nautico, Farmaceutico, Cosmetico, Tecnologico. Dammi una risposta con solo la parola del settore, solo se corirsponde senno rispondi NO, non voglio altre parole, una sola parola come risposta.",
    "Da quanti anni è aperta e attiva la azienda?": "Convertimi il numero in un numero intero che si avvicina di piu alla risposta, se non riescei rispondi solo NO, la risposta deve essere solo composta da un numero.",
    "Su quali piattaforme social media è attualmente presente la vostra azienda?": "Valuta la risposta fornita e dammi una risposta costituita dai nomi dei social network corretti seguiti da una , non devi aggiungere altre parole, se nessun social network e stato fornito rispondi NO",
    "Avete già condotto campagne di marketing sui social media per mercati internazionali? Se sì, quali?": "Analizza la risposta e forniscimi i concetti chiavi delimitati da una virgola in caso non ci sia nulla rispondimi solo con un NO",
    "Quali sono le vostre maggiori preoccupazioni riguardo l'esportazione in nuovi mercati?": "Analizza la risposta e forniscimi i concetti chiavi delimitati da una virgola in caso non ci sia nulla rispondimi solo con un NO",
    "Quale prodotto e/o prodotti vorresti esportare?": "Analizza la sentenza e fornisci una lista di prodotti. Se ci sono più prodotti, separali con una virgola. Se non vi sono prodotti identificabili, scrivi NO. La risposta deve contenere solo i nomi dei prodotti o NO.",
    "Vuoi spostare la produzione all'estero?": "Valuta la frase e valuta se è positiva, se è positiva rispondimi SI, sennò rispondimi solamente NO",
    "Vuoi trovare nuovi fornitori per il tuo mercato?": "Valuta la frase e valuta se è positiva, se è positiva rispondimi SI, sennò rispondimi solamente NO"
}

def preprocess_products(user_response):
    # Sostituisce congiunzioni comuni con virgole
    for conjunction in [' e ', ' ed ', ' & ', ' + ']:
        user_response = user_response.replace(conjunction, ', ')
    # Rimuove spazi extra e divide per virgola
    products = [p.strip() for p in user_response.split(',') if p.strip()]
    return ', '.join(products) if products else user_response

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

    if "Quale prodotto e/o prodotti vorresti esportare?" in question:
        user_response = preprocess_products(user_response)

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
        db = get_db()
        c = db.cursor()
        c.execute("INSERT INTO responses (question, user_response, llm_analysis) VALUES (?, ?, ?)",
                  (question, user_response, llm_analysis))
        db.commit()
        return jsonify({"success": True, "message": "Risposta analizzata e salvata con successo"})

@app.route('/get_data', methods=['GET'])
def get_data():
    db = get_db()
    c = db.cursor()
    
    c.execute("SELECT question, user_response, llm_analysis FROM responses")
    
    data = c.fetchall()
    
    formatted_data = [{"question": row[0], "user_response": row[1], "llm_analysis": row[2]} for row in data]
    
    return jsonify(formatted_data)

@app.route('/get_db_uuid', methods=['GET'])
def get_db_uuid_route():
    if DEBUG_MODE:
        return jsonify({"db_uuid": get_db_uuid()})
    else:
        return jsonify({"message": "Debug mode is not enabled"}), 403

if __name__ == '__main__':
    app.run(debug=DEBUG_MODE)
