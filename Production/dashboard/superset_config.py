import os

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:supersecretpassword@postgres:5432/superset'
REDIS_HOST = 'redis'
REDIS_PORT = 6379

# Abilita l'accesso da qualsiasi IP
SUPERSET_WEBSERVER_ADDRESS = "0.0.0.0"

# Configurazione per l'accesso pubblico
from flask_appbuilder.security.manager import AUTH_DB

AUTH_TYPE = AUTH_DB
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Public"
PUBLIC_ROLE_LIKE = "Gamma"
PUBLIC_ROLE_LIKE_GAMMA = True
FEATURE_FLAGS = {
    "ANONYMOUS_IN_DASHBOARDS": True,
    "ENABLE_TEMPLATE_PROCESSING": True,
}
ANONYMOUS_REDIRECT_URL = "/superset/welcome/"
SESSION_COOKIE_SAMESITE = None

# Configurazione per il plugin RAG Chatbot
CUSTOM_TEMPLATE_PROCESSORS = {
    'rag_chatbot': 'superset_rag_plugin.superset_rag_chatbot.plugin.ChatbotViz',
}