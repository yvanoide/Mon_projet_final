import jwt
import bcrypt
import datetime
from pymongo import MongoClient

# Clés de sécurité
SECRET_KEY = "12345"

# Connexion à MongoDB
client = MongoClient('mongodb://root:pass12345@localhost:27017/')
db = client["connexion"]
patients = db["patient"]

# Ajouter un patient dans la base de données
def register_patient(prenom, mot_de_passe, email):
    hashed_password = bcrypt.hashpw(mot_de_passe.encode(), bcrypt.gensalt()).decode()  # Encode en bytes puis décode en str
    patient = {
        "prenom": prenom,
        "mot_de_passe": hashed_password,
        "email": email
    }
    patients.insert_one(patient)
    print(f"Patient {prenom} enregistré avec succès.")

# Vérification des informations d'authentification et génération d'un token JWT
def authenticate_patient(email, mot_de_passe):
    patient = patients.find_one({"email": email})
    if patient:
        # Convertir le mot de passe stocké en bytes avant la vérification
        hashed_password = patient["mot_de_passe"].encode()  # Reconvertir en bytes
        if bcrypt.checkpw(mot_de_passe.encode(), hashed_password):  # Comparer les mots de passe
            token = create_token(patient["prenom"], "patient", email)
            return token
    return "Email ou mot de passe incorrect."

# Génération d'un JWT
def create_token(prenom, role, email):
    payload = {
        "prenom": prenom,
        "role": role,
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# Décodage et vérification du JWT
def decode_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return "Token expiré"
    except jwt.InvalidTokenError:
        return "Token invalide"

# Exemple d'utilisation
if __name__ == "__main__":
    # Enregistrer un patient
    print("Enregistrement de Gérard...")
    register_patient("Gérard", "ademain", "demain@hotmail.fr")

    # Authentifier un patient
    print("\nAuthentification de Gérard...")
    token = authenticate_patient("demain@hotmail.fr", "ademain")
    print(f"Token généré pour Gérard: {token}")

    # Décoder le token
    if token != "Email ou mot de passe incorrect.":
        print("\nDécodage du token...")
        decoded_data = decode_token(token)
        print(f"Données décodées : {decoded_data}")
    else:
        print("Impossible d'authentifier l'utilisateur.")
