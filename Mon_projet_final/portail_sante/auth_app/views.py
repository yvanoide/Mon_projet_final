from django.shortcuts import render, redirect
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError
import pandas as pd
import tensorflow as tf
import joblib
import os
import requests
from django.http import JsonResponse

# Configurer les paramètres de connexion MongoDB
MONGO_URI = 'mongodb://root:pass12345@localhost:27017/'
DATABASE_NAME = 'connexion'
COLLECTION_NAME = 'patient'

def connect_to_mongo():
    try:
        # Se connecter à MongoDB
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        return collection
    except ServerSelectionTimeoutError as e:
        print(f"Erreur de connexion à MongoDB : {e}")
        return None
    except PyMongoError as e:
        print(f"Erreur MongoDB : {e}")
        return None
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        return None

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        prenom = request.POST.get('prenom')
        mot_de_passe = request.POST.get('mot_de_passe')
        
        # Connexion à MongoDB
        collection = connect_to_mongo()
        
        if collection is None:
            return render(request, 'login.html', {'error': 'Erreur de connexion à la base de données.'})
        
        # Trouver le patient dans MongoDB
        patient = collection.find_one({'prenom': prenom, 'mot_de_passe': mot_de_passe})
        if patient:
            return redirect('connexion_reussie')
        else:
            return render(request, 'login.html', {'error': 'Connexion échouée, réessayez.'})
    
    return render(request, 'login.html')

def connexion_reussie(request):
    return render(request, 'connexion_reussie.html')

# Fonction personnalisée utilisée dans le modèle
def custom_accuracy(y_true, y_pred):
    return tf.keras.metrics.binary_accuracy(y_true, y_pred)

# Fonction pour charger le modèle et le préprocesseur
def load_model_and_preprocessor():
    try:
        model_path = os.path.join(os.path.dirname(__file__), 'best_model.keras')
        preprocessor_path = os.path.join(os.path.dirname(__file__), 'preprocessor.joblib')
        model = tf.keras.models.load_model(model_path, custom_objects={'custom_accuracy': custom_accuracy})
        preprocessor = joblib.load(preprocessor_path)
        return model, preprocessor
    except Exception as e:
        print(f"Erreur lors du chargement du modèle ou du préprocesseur : {e}")
        return None, None

# Charger le modèle et le préprocesseur
model, preprocessor = load_model_and_preprocessor()

def service_monitoring(request):
    monitoring_status = {
        'mongodb_connection': False,
        'model_load': False,
    }

    # Vérification de la connexion MongoDB
    try:
        collection = connect_to_mongo()
        if collection is not None:
            monitoring_status['mongodb_connection'] = True
    except Exception as e:
        print(f"Erreur lors de la vérification de MongoDB : {e}")

    # Vérification du chargement du modèle
    monitoring_status['model_load'] = model is not None

    # Retourner l'état du monitoring sous forme de réponse JSON
    if monitoring_status['mongodb_connection'] and monitoring_status['model_load']:
        return JsonResponse({'status': 'operational', 'details': monitoring_status}, status=200)
    else:
        return JsonResponse({'status': 'non-operational', 'details': monitoring_status}, status=500)

def equipe_view(request):
    return render(request, 'equipe.html')

def directeur(request):
    return render(request, 'directeur.html')

# Votre URL d'API FastAPI
FASTAPI_URL = 'http://localhost:8002'

# Fonction pour obtenir le jeton JWT
def get_token():
    url = f'{FASTAPI_URL}/token'
    data = {
        'username': 'user',  # Nom d'utilisateur par défaut
        'password': 'password'  # Mot de passe par défaut
    }
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        return None

# Fonction pour obtenir la prédiction depuis l'API FastAPI
def get_prediction_from_api(data):
    token = get_token()
    if not token:
        return None  # Gérer l'erreur si le token n'est pas récupéré correctement

    url = f'{FASTAPI_URL}/predict'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'  # Ajouter le jeton JWT dans les en-têtes
    }
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Retourne la prédiction sous forme de dictionnaire
    else:
        return None

def test(request):
    result = None
    if request.method == 'POST':
        # Extraction des données du formulaire
        genre = request.POST.get('genre')
        age = request.POST.get('age')
        sleep_quality = float(request.POST.get('sleep_quality')) / 100.0  # Convertir en décimal
        heart_rate = request.POST.get('heart_rate')
        steps = request.POST.get('steps')
        sleep_duration = request.POST.get('sleep_duration')

        # Préparer les données à envoyer à l'API FastAPI
        data = {
            'genre': genre,
            'age': age,
            'sleep_quality': sleep_quality,
            'heart_rate': heart_rate,
            'steps': steps,
            'sleep_duration': sleep_duration
        }

        # Obtenir la prédiction depuis l'API FastAPI
        result = get_prediction_from_api(data)

    return render(request, 'test.html', {
        'result': result, 
        'score': result['score'] if result else None, 
        'response': result['response'] if result else None
    })

import mlflow
import mlflow.keras

# Fonction d'entraînement avec MLflow
def train_model_with_mlflow(data, labels):
    with mlflow.start_run():
        # Suivi des paramètres d'entraînement
        mlflow.log_param('batch_size', 32)
        mlflow.log_param('epochs', 10)
        
        # Charger le modèle et l'entraîner
        model = create_model()  # Fonction qui crée votre modèle
        history = model.fit(data, labels, epochs=10, batch_size=32)
        
        # Enregistrer les métriques de performance
        mlflow.log_metric('accuracy', history.history['accuracy'][-1])
        mlflow.log_metric('loss', history.history['loss'][-1])
        
        # Enregistrer le modèle avec MLflow
        mlflow.keras.log_model(model, 'model')

        return model
