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
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
from fastapi.encoders import jsonable_encoder
from pymongo.errors import PyMongoError

# Configuration FastAPI principale
app = FastAPI()

# Configuration MongoDB
MONGO_URI = 'mongodb://root:pass12345@localhost:27017/'
DATABASE_NAME = 'data'
COLLECTION_NAME = 'bigdata'

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Configuration du modèle TensorFlow
MODEL_PATH = '/home/yves/iadev-python/c8/best_model.keras'
PREPROCESSOR_PATH = '/home/yves/iadev-python/c8/preprocessor.joblib'

# Charger le modèle et le préprocesseur
try:
    model = tf.keras.models.load_model(
        MODEL_PATH,
        custom_objects={'custom_accuracy': tf.keras.metrics.binary_accuracy}
    )
    preprocessor = joblib.load(PREPROCESSOR_PATH)
except Exception as e:
    model = None
    preprocessor = None
    print(f"Erreur lors du chargement des fichiers : {e}")

# JWT Configuration
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Cache de prédiction
cache = TTLCache(maxsize=100, ttl=300)

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

# MongoDB Data Model
class DataSante(BaseModel):
    genre: str
    age: int
    qualite_sommeil: float
    rythme_cardiaque: int
    etapes_quotidiennes: int
    duree_sommeil: float
    score_sante: float

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token invalide")

# Authentification et token
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "user" and form_data.password == "password":
        access_token = create_access_token(
            data={"sub": form_data.username},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Identifiants invalides")

def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)

# CRUD routes pour MongoDB
@app.get("/data/{id}")
async def get_data_by_id(id: str):
    try:
        object_id = ObjectId(id)
        document = collection.find_one({"_id": object_id})
        if document is None:
            raise HTTPException(status_code=404, detail="Data not found")
        document["_id"] = str(document["_id"])
        return document
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    except PyMongoError:
        raise HTTPException(status_code=500, detail="Database error")

@app.post("/data_sante/")
async def create_data(data: DataSante):
    try:
        data_dict = jsonable_encoder(data)
        result = collection.insert_one(data_dict)
        return {"_id": str(result.inserted_id), **data_dict}
    except PyMongoError:
        raise HTTPException(status_code=500, detail="Database error")

@app.put("/data_sante/{id}")
async def update_data(id: str, data: DataSante):
    try:
        updated_data = {k: v for k, v in data.dict().items() if v is not None}
        result = collection.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
        if result.modified_count:
            return {"_id": id, **updated_data}
        raise HTTPException(status_code=404, detail="Data not found")
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    except PyMongoError:
        raise HTTPException(status_code=500, detail="Database error")

@app.delete("/data_sante/{id}")
async def delete_data(id: str):
    try:
        result = collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return {"detail": "Data deleted successfully"}
        raise HTTPException(status_code=404, detail="Data not found")
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    except PyMongoError:
        raise HTTPException(status_code=500, detail="Database error")

# Prédiction
@app.post("/predict")
async def predict(request: PredictionRequest, current_user: dict = Depends(get_current_user)):
    if model is None or preprocessor is None:
        raise HTTPException(status_code=500, detail="Modèle ou préprocesseur non chargé.")
    try:
        data = pd.DataFrame([{
            'Genre': request.genre,
            'Âge': request.age,
            'Qualité du sommeil': request.sleep_quality / 100.0,
            'Rythme cardiaque': request.heart_rate,
            'Étapes quotidiennes': request.steps,
            'Durée du sommeil': request.sleep_duration
        }])
        transformed_data = preprocessor.transform(data)
        predictions = model.predict(transformed_data)
        score = predictions[0][0].item()
        response = 0.75
        if score <= 0.24:
            response = 0
        elif 0.25 <= score <= 0.4:
            response = 0.25
        elif 0.41 <= score <= 0.5:
            response = 0.5
        return {"score": float(score), "response": float(response)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur : {str(e)}")

@app.get("/health")
async def health_check():
    if model is None or preprocessor is None:
        raise HTTPException(status_code=500, detail="Modèle ou préprocesseur non chargé.")
    try:
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
