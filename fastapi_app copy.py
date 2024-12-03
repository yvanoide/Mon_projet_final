from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from pymongo import MongoClient
import jwt
import datetime
from typing import Optional

# Connexion à MongoDB
client = MongoClient('mongodb://root:pass12345@localhost:27017/')
db = client["connexion"]
patients = db["patient"]

app = FastAPI()

# Clé secrète pour signer le JWT
SECRET_KEY = "votre_clé_secrète"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 30  # Durée de validité du token en minutes

# Modèle Pydantic pour valider la structure de la demande de connexion
class UserLogin(BaseModel):
    prenom: str
    mot_de_passe: str

# Modèle pour retourner le token
class Token(BaseModel):
    access_token: str
    token_type: str

# Fonction pour créer le JWT
def create_access_token(prenom: str):
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=EXPIRE_MINUTES)
    to_encode = {"sub": prenom, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Fonction pour vérifier le token JWT
def verify_token(token: str):
    try:
        # Décoder le token et vérifier sa signature
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Vérifier que le token n'est pas expiré
        if datetime.datetime.utcnow() > datetime.datetime.fromtimestamp(payload["exp"]):
            raise HTTPException(status_code=401, detail="Le token a expiré")
        return payload["sub"]  # Retourne le prénom de l'utilisateur
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Le token a expiré")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")

# Route pour la connexion
@app.post("/login", response_model=Token)
async def login(user: UserLogin):
    # Recherche de l'utilisateur dans MongoDB par son prénom
    patient = patients.find_one({"prenom": user.prenom})
    
    # Si l'utilisateur n'existe pas, retourner une erreur
    if not patient:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # Vérifier le mot de passe
    if patient["mot_de_passe"] != user.mot_de_passe:
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")

    # Générer un token JWT valide
    access_token = create_access_token(user.prenom)
    return {"access_token": access_token, "token_type": "bearer"}

# Route protégée : Exemple d'accès avec un token valide
@app.get("/protected")
def protected_route(token: str = Depends(verify_token)):
    return {"message": f"Bienvenue {token}, vous avez accédé à une route protégée."}
