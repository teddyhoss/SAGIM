# Superset con RAG Chatbot - Setup e Deployment

## Prerequisiti

1. Docker e Docker Compose V2 installati
2. Un token valido per l'API Regolo AI

## Setup Iniziale

1. Crea un file `.env` nella directory principale con il seguente contenuto:

   ```
   POSTGRES_DB=superset
   POSTGRES_PASSWORD=supersecretpassword
   SUPERSET_SECRET_KEY=your_very_secure_secret_key_here
   REGOLO_TOKEN=your_regolo_token_here
   ```

2. Assicurati che la directory `superset_rag_plugin` con il codice del plugin RAG chatbot sia presente.

3. Verifica che il file `init_data.sql` con i dati mockup sia nella directory principale.

## Passi per il Deployment

1. Avvia i container:
   ```
   docker compose up -d
   ```

2. Attendi circa 30 secondi per assicurarti che tutti i servizi siano pronti.

3. Inizializza il database di Superset:
   ```
   docker compose exec superset superset db upgrade
   ```

4. Crea un account admin:
   ```
   docker compose exec superset superset fab create-admin \
       --username admin \
       --firstname Admin \
       --lastname User \
       --email admin@example.com \
       --password admin_password
   ```

5. Inizializza Superset:
   ```
   docker compose exec superset superset init
   ```

6. Crea i permessi e il ruolo pubblico:
   ```
   docker compose exec superset superset fab create-permissions
   docker compose exec superset superset init
   ```

7. Installa il plugin RAG chatbot:
   ```
   docker compose exec superset pip install -e /app/superset_rag_plugin
   ```

8. Riavvia Superset per attivare il plugin:
   ```
   docker compose restart superset
   ```

## Accesso a Superset

Dopo aver completato questi passaggi, Superset sarà accessibile all'indirizzo:

```
http://your_vps_ip:8088
```

Utilizza le seguenti credenziali per accedere come amministratore:
- Username: admin
- Password: admin_password

## Note Importanti

1. **Sicurezza**: Modifica la password dell'admin e il `SUPERSET_SECRET_KEY` nel file `.env` prima di utilizzare Superset in produzione.
2. **Dati Mockup**: I dati mockup sono caricati automaticamente nel database PostgreSQL all'avvio. Puoi modificare questi dati nel file `init_data.sql`.
3. **Plugin RAG Chatbot**: Il chatbot è accessibile tramite l'endpoint `/rag-chatbot/query`. Assicurati di implementare le necessarie misure di sicurezza prima di esporlo pubblicamente.
4. **API Regolo**: Assicurati di avere un token valido per l'API Regolo e di averlo inserito correttamente nel file `.env`.

## Risoluzione dei Problemi

Se incontri problemi durante il deployment:

1. Controlla i log dei container:
   ```
   docker compose logs
   ```

2. Assicurati che tutte le porte necessarie siano aperte e accessibili.

3. Verifica che i servizi siano in esecuzione:
   ```
   docker compose ps
   ```

Per ulteriore assistenza, consulta la documentazione ufficiale di Apache Superset o chiedi supporto alla community.
