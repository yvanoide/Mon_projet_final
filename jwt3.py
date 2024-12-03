import jwt
import bcrypt
import datetime
from pymongo import MongoClient

# Clé secrète pour le JWT
SECRET_KEY = "12345"

# Connexion à MongoDB
client = MongoClient('mongodb://root:pass12345@localhost:27017/')
db = client["connexion"]
patients = db["patient"]

# Fonction pour enregistrer un utilisateur
def register_patient(prenom, mot_de_passe, email):
    # Vérification si l'email existe déjà
    patient_existant = patients.find_one({"email": email})
    
    if patient_existant:  # Si l'email est trouvé, on ne réenregistre pas
        print(f"L'email {email} est déjà enregistré pour {patient_existant['prenom']}.")
        return patient_existant  # Retourne les données de l'utilisateur existant
    
    # Si l'email n'existe pas, on procède à l'enregistrement
    hashed_password = bcrypt.hashpw(mot_de_passe.encode(), bcrypt.gensalt())
    patient = {
        "prenom": prenom,
        "mot_de_passe": hashed_password,
        "email": email
    }
    patients.insert_one(patient)
    print(f"Patient {prenom} enregistré avec succès.")
    return patient

# Fonction pour générer un token JWT
def create_token(prenom, role, email):
    payload = {
        "prenom": prenom,
        "role": role,
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# Fonction pour vérifier un token JWT
def decode_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return "Token expiré"
    except jwt.InvalidTokenError:
        return "Token invalide"

# Programme principal interactif
if __name__ == "__main__":
    # Enregistrement ou récupération de l'utilisateur
    print("=== Enregistrement ou Connexion ===")
    prenom = input("Entrez votre prénom : ")
    mot_de_passe = input("Entrez votre mot de passe : ")
    email = input("Entrez votre email : ")
    
    # Vérifie si l'email existe et enregistre ou récupère l'utilisateur
    patient = register_patient(prenom, mot_de_passe, email)
    
    # Génération du token
    token = create_token(patient["prenom"], "patient", patient["email"])
    print(f"\nVoici votre token JWT : {token}\n")
    
    # Validation du token
    print("=== Validation du Token ===")
    token_entre = input("Entrez votre token : ")
    
    # Vérification
    decoded = decode_token(token_entre)
    if isinstance(decoded, dict) and decoded.get("prenom") == prenom:
        print("Token valide !")
        print(f"Données décodées : {decoded}")
    else:
        print("Token invalide.")
