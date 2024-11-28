import jwt
import datetime

# Clé secrète pour signer les tokens
SECRET_KEY = "12345"

# Base de données utilisateur simulée
USERS = {
    "Jacques": {"role": "admin", "password": "utilite18"},
    "directeur": {"role": "directeur", "password": "directiondesusers"},
}

# Création d'un JWT
def create_token(username, role):
    payload = {
        "username": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expire en 1 heure
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# Authentification utilisateur
def authenticate_user(username, password):
    user = USERS.get(username)
    if user and user["password"] == password:
        return create_token(username, user["role"])
    return None

# Décodage et vérification du JWT
def decode_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded  # Données décodées
    except jwt.ExpiredSignatureError:
        return "Token expiré"
    except jwt.InvalidTokenError:
        return "Token invalide"

# Test interactif
if __name__ == "__main__":
    print("Authentification de Jacques...")
    username = "Jacques"
    password = "utilite18"

    # Authentifier l'utilisateur
    token = authenticate_user(username, password)
    if token:
        print(f"Token généré pour {username}: {token}")
        
        print("\nDécodage du token...")
        decoded = decode_token(token)
        print(f"Données décodées: {decoded}")
    else:
        print("Échec d'authentification : identifiant ou mot de passe incorrect.")
