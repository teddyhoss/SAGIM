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

## Accesso a Superset

Dopo aver completato questi passaggi, Superset sarà accessibile all'indirizzo:

```
http://your_vps_ip:8088
```

Utilizza le seguenti credenziali per accedere come amministratore:
- Username: admin
- Password: admin_password

## Note Importanti

1. **Sicurezza**: Modifica la password dell'admin e il `SUPERSET_SECRET_KEY` nel file `docker-compose.yml` prima di utilizzare Superset in produzione.
