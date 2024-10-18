from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import tensorflow as tf
import joblib
import pandas as pd
import os
import numpy as np
from datetime import datetime, timedelta
import jwt
from cachetools import cached, TTLCache
app = FastAPI()

# Configuration des clés secrètes et des paramètres d'authentification
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Chemins des fichiers
MODEL_PATH = '/home/yves/iadev-python/c8/best_model.keras'
PREPROCESSOR_PATH = '/home/yves/iadev-python/c8/preprocessor.joblib'

# Assurez-vous que le modèle et le préprocesseur existent
if not os.path.isfile(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
if not os.path.isfile(PREPROCESSOR_PATH):
    raise FileNotFoundError(f"Preprocessor file not found: {PREPROCESSOR_PATH}")

# Définir la fonction personnalisée
@tf.keras.utils.register_keras_serializable()
def custom_accuracy(y_true, y_pred):
    return tf.keras.metrics.binary_accuracy(y_true, y_pred)

# Charger le modèle
try:
    model = tf.keras.models.load_model(
        MODEL_PATH,
        custom_objects={'custom_accuracy': custom_accuracy}
    )
    print("Modèle chargé avec succès.")
except Exception as e:
    print(f"Erreur lors du chargement du modèle : {e}")
    model = None

# Charger le préprocesseur
try:
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    print("Préprocesseur chargé avec succès.")
except Exception as e:
    print(f"Erreur lors du chargement du préprocesseur : {e}")
    preprocessor = None

class PredictionRequest(BaseModel):
    genre: str
    age: int
    sleep_quality: float
    heart_rate: int
    steps: int
    sleep_duration: float

class User(BaseModel):
    username: str
    password: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token invalide")
cache = TTLCache(maxsize=100, ttl=300)  # Cache de 100 éléments avec une expiration de 5 minutes

#@cached(cache)
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Ici, vous devriez vérifier les informations d'identification de l'utilisateur
    if form_data.username == "user" and form_data.password == "password":
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Identifiants invalides")

def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)

@app.post("/predict")
async def predict(request: PredictionRequest, current_user: dict = Depends(get_current_user)):
    if model is None or preprocessor is None:
        raise HTTPException(status_code=500, detail="Modèle ou préprocesseur non chargé.")

    try:
        # Convertir les données d'entrée en DataFrame
        data = pd.DataFrame([{
            'Genre': request.genre,
            'Âge': request.age,
            'Qualité du sommeil': request.sleep_quality / 100.0,  # Convertir en décimal
            'Rythme cardiaque': request.heart_rate,
            'Étapes quotidiennes': request.steps,
            'Durée du sommeil': request.sleep_duration
        }])

        # Vérifiez les données avant le prétraitement
        print("Données avant prétraitement:", data)

        # Appliquer le prétraitement
        transformed_data = preprocessor.transform(data)

        # Vérifiez les données après le prétraitement
        print("Données transformées:", transformed_data)

        # Faire la prédiction
        predictions = model.predict(transformed_data)
        score = predictions[0][0].item()  # Convertir numpy.float32 en float natif
        response = 0.75  # Valeur par défaut

        # Déterminer la réponse en fonction du score
        if score <= 0.24:
            response = 0
        elif 0.25 <= score <= 0.4:
            response = 0.25
        elif 0.41 <= score <= 0.5:
            response = 0.5
        else:
            response = 0.75

        return {"score": float(score), "response": float(response)}  # Convertir en float natif pour JSON

    except Exception as e:
        print(f"Erreur : {str(e)}")  # Ajouter un log d'erreur
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur : {str(e)}")

@app.get("/health")
async def health_check():
    if model is None or preprocessor is None:
        raise HTTPException(status_code=500, detail="Modèle ou préprocesseur non chargé.")
    
    try:
        # Test du modèle
        test_data = pd.DataFrame([{
            'Genre': 'Male',
            'Âge': 30,
            'Qualité du sommeil': 0.5,
            'Rythme cardiaque': 70,
            'Étapes quotidiennes': 5000,
            'Durée du sommeil': 8
        }])
        transformed_test_data = preprocessor.transform(test_data)
        model.predict(transformed_test_data)
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Échec de la vérification du modèle : {str(e)}")
