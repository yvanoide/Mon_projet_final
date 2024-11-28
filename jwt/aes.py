import jwt
import datetime
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

# Clé secrète pour JWT
SECRET_KEY_JWT = "12345"

# Génération d'une clé AES pour le chiffrement (32 octets pour AES-256)
AES_KEY = get_random_bytes(32)

# Utilisateurs (base de données simulée)
USERS = {
    "Jacques": {"role": "admin", "password": "utilite18"},
    "directeur": {"role": "directeur", "password": "directiondesusers"},
}

# Fonctions pour le chiffrement et déchiffrement AES
def encrypt_data(data):
    """Chiffre les données avec AES."""
    cipher = AES.new(AES_KEY, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

def decrypt_data(enc_data):
    """Déchiffre les données AES."""
    enc_data = base64.b64decode(enc_data)
    nonce, tag, ciphertext = enc_data[:16], enc_data[16:32], enc_data[32:]
    cipher = AES.new(AES_KEY, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()

# Création d'un JWT
def create_token(username, role):
    """Crée un token JWT avec des données sensibles chiffrées."""
    sensitive_data = {
        "username": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
    }
    encrypted_data = encrypt_data(str(sensitive_data))  # Chiffrement des données
    payload = {"encrypted": encrypted_data}
    return jwt.encode(payload, SECRET_KEY_JWT, algorithm="HS256")

# Décodage et vérification du JWT
def decode_token(token):
    """Décode le JWT et déchiffre les données."""
    try:
        payload = jwt.decode(token, SECRET_KEY_JWT, algorithms=["HS256"])
        encrypted_data = payload.get("encrypted", "")
        return decrypt_data(encrypted_data)  # Déchiffrement des données
    except jwt.ExpiredSignatureError:
        return "Token expiré"
    except jwt.InvalidTokenError:
        return "Token invalide"
    except Exception as e:
        return f"Erreur de déchiffrement : {e}"

# Authentification utilisateur
def authenticate_user(username, password):
    """Vérifie les identifiants utilisateur et génère un token JWT."""
    user = USERS.get(username)
    if user and user["password"] == password:
        return create_token(username, user["role"])
    return None

# Main
if __name__ == "__main__":
    # Exemple : Authentification de Jacques
    print("Authentification de Jacques...")
    token = authenticate_user("Jacques", "utilite18")
    if token:
        print(f"Token généré pour Jacques: {token}\n")
        print("Décodage du token...")
        decoded_data = decode_token(token)
        print(f"Données décodées : {decoded_data}")
    else:
        print("Échec d'authentification : identifiant ou mot de passe incorrect.")

