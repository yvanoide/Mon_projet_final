import jwt
import datetime
import pytest

# Variables de configuration
SECRET_KEY = "12345"
USERS = {
    "Jacques": {"role": "admin", "password": "utilite18"},
    "directeur": {"role": "directeur", "password": "directiondesusers"},
}

# Fonctions à tester
def create_token(username, role):
    payload = {
        "username": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expire en 1 heure
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def authenticate_user(username, password):
    user = USERS.get(username)
    if user and user["password"] == password:
        return create_token(username, user["role"])
    return None

def decode_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded  # Données décodées
    except jwt.ExpiredSignatureError:
        return "Token expiré"
    except jwt.InvalidTokenError:
        return "Token invalide"

# Tests
def test_authentication_success():
    """Tester l'authentification réussie et la génération du token."""
    username = "Jacques"
    password = "utilite18"
    token = authenticate_user(username, password)
    assert token is not None, "Token should not be None"
    
    # Décodage du token et validation des données
    decoded = decode_token(token)
    assert decoded["username"] == username, f"Expected username {username}, but got {decoded['username']}"
    assert decoded["role"] == "admin", f"Expected role 'admin', but got {decoded['role']}"
    assert "exp" in decoded, "Expected 'exp' (expiration) field in the decoded token"

def test_authentication_failure_invalid_password():
    """Tester l'échec de l'authentification avec un mot de passe incorrect."""
    username = "Jacques"
    password = "wrongpassword"
    token = authenticate_user(username, password)
    assert token is None, "Token should be None for incorrect password"

def test_token_expiry():
    """Tester le décodage d'un token expiré."""
    username = "Jacques"
    password = "utilite18"
    token = authenticate_user(username, password)
    
    # Simuler une expiration du token
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
    expired_token = jwt.encode(
        {**payload, "exp": datetime.datetime.utcnow() - datetime.timedelta(hours=1)},
        SECRET_KEY,
        algorithm="HS256"
    )

    decoded = decode_token(expired_token)
    assert decoded == "Token expiré", f"Expected 'Token expiré', but got {decoded}"

def test_invalid_token():
    """Tester un token invalide."""
    invalid_token = "this_is_an_invalid_token"
    decoded = decode_token(invalid_token)
    assert decoded == "Token invalide", f"Expected 'Token invalide', but got {decoded}"
