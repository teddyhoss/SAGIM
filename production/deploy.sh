#!/bin/bash

# Caricare le immagini
echo "Caricamento delle immagini Docker..."
docker load -i sagim_dash_image.tar
docker load -i pgsql_general_image.tar
docker load -i superset_db_image.tar
docker load -i superset_redis_image.tar
docker load -i superset_image.tar

# Importare i container (se necessario)
echo "Importazione dei container..."
docker import sagim_dash_container.tar
docker import pgsql_general_container.tar
docker import superset_db_container.tar
docker import superset_redis_container.tar
docker import superset_container.tar

# Avviare i container
echo "Avvio dei container..."
docker run -d --name sagim_dash sagim-dash
docker run -d --name pgsql_general -p 5432:5432 postgres:latest
docker run -d --name superset_db -p 5433:5432 postgres:12
docker run -d --name superset_redis -p 6379:6379 redis:latest
docker run -d --name superset -p 8088:8088 apache/superset:latest

echo "Tutti i container sono stati avviati!"
