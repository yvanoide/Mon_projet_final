import os
import bcrypt
import jwt
import datetime
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, validator
from pymongo import MongoClient
from dotenv import load_dotenv

# Charger les variables d'environnement à partir d'un fichier .env
load_dotenv()

# Configuration MongoDB
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["connexion"]
patients = db["patient"]

# Configuration du JWT
SECRET_KEY = os.getenv("SECRET_KEY", "12345")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 1

# Création de l'application FastAPI
app = FastAPI()

# Définir l'OAuth2PasswordBearer pour l'authentification
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Modèles de requêtes
class RegisterRequest(BaseModel):
    prenom: str
    mot_de_passe: str

    @validator("mot_de_passe")
    def validate_password(cls, mot_de_passe):
        if len(mot_de_passe) < 8:
            raise ValueError("Le mot de passe doit contenir au moins 8 caractères.")
        if not any(char.islower() for char in mot_de_passe):
            raise ValueError("Le mot de passe doit contenir au moins une minuscule.")
        if not any(char.isupper() for char in mot_de_passe):
            raise ValueError("Le mot de passe doit contenir au moins une majuscule.")
        if not any(char.isdigit() for char in mot_de_passe):
            raise ValueError("Le mot de passe doit contenir au moins un chiffre.")
        return mot_de_passe


class LoginRequest(BaseModel):
    prenom: str
    mot_de_passe: str


class TokenResponse(BaseModel):
    token: str


# Fonction pour générer un token JWT
def create_token(prenom: str):
    payload = {
        "prenom": prenom,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


# Fonction pour récupérer l'utilisateur actuel à partir du token JWT
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("prenom")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expiré")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalide")


# Route : Enregistrer un nouvel utilisateur
@app.post("/register", response_model=TokenResponse, summary="Enregistrer un nouvel utilisateur")
def register_patient(request: RegisterRequest):
    # Vérifie si le prénom existe déjà
    existing_patient = patients.find_one({"prenom": request.prenom})
    if existing_patient:
        raise HTTPException(status_code=400, detail="Prénom déjà enregistré")
    
    # Hache le mot de passe
    hashed_password = bcrypt.hashpw(request.mot_de_passe.encode(), bcrypt.gensalt()).decode()

    # Insère l'utilisateur dans la base de données
    patient = {
        "prenom": request.prenom,
        "mot_de_passe": hashed_password
    }
    patients.insert_one(patient)

    # Génère un token pour le nouvel utilisateur
    token = create_token(request.prenom)
    return {"token": token}


# Route : Connexion d'un utilisateur existant
@app.post("/login", response_model=TokenResponse, summary="Connexion d'un utilisateur")
def login_patient(request: LoginRequest):
    # Récupère l'utilisateur par prénom
    patient = patients.find_one({"prenom": request.prenom})
    if not patient:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # Vérifie le mot de passe
    if not bcrypt.checkpw(request.mot_de_passe.encode(), patient["mot_de_passe"].encode()):
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")

    # Génère un token
    token = create_token(request.prenom)
    return {"token": token}


# Route protégée : Exemple d'accès avec un token valide
@app.get("/protected", summary="Route protégée")
def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Bienvenue {current_user}, vous avez accédé à une route protégée."}
