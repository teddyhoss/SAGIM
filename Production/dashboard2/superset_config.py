from flask_appbuilder.security.manager import AUTH_DB

AUTH_TYPE = AUTH_DB
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Public"
PUBLIC_ROLE_LIKE = "Gamma"
PUBLIC_ROLE_LIKE_GAMMA = True

FEATURE_FLAGS = {
    "DASHBOARD_RBAC": False,
    "ENABLE_TEMPLATE_PROCESSING": True,
}

GUEST_ROLE_NAME = "Public"
GUEST_TOKEN_JWT_SECRET = "my-custom-secret"  # Cambia questo con una stringa segreta sicura
GUEST_TOKEN_JWT_ALGO = "HS256"
GUEST_TOKEN_HEADER_NAME = "X-GuestToken"
ENABLE_PROXY_FIX = True