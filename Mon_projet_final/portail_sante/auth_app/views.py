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

from django.shortcuts import render, redirect
from django.contrib import messages
from pymongo import MongoClient

# Assurez-vous que vous avez installé pymongo : pip install pymongo

from django.shortcuts import render, redirect
from pymongo import MongoClient


def directeur(request):
    if request.method == 'POST':
        # Ici, vous devriez récupérer les données du formulaire
        utilisateur = request.POST.get('utilisateur')
        mot_de_passe = request.POST.get('mot_de_passe')

        # Connexion à la base de données MongoDB
        MONGO_URI = "mongodb://root:pass12345@localhost:27017/"
        client = MongoClient(MONGO_URI)
        db = client.connexion
        collection = db.super_admin

        # Vérifiez si les informations d'identification sont correctes
        admin = collection.find_one({"utilisateur": utilisateur, "mot_de_passe": mot_de_passe})

        if admin:
            # Redirige vers la page de succès
            return redirect('directeur_reussi')
        else:
            # Gérer l'erreur (redirection ou message d'erreur)
            return render(request, 'directeur.html', {'error': 'Identifiants invalides'})

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
    user_prenom = None

    # Configuration de MongoDB
    MONGO_URI = 'mongodb://root:pass12345@localhost:27017/'
    DATABASE_NAME = 'connexion'
    COLLECTION_RESULTAT = 'resultat_test'

    # Vérifier si l'utilisateur est connecté
    if 'prenom' in request.session:
        user_prenom = request.session['prenom']

    if request.method == 'POST':
        # Extraire les données du formulaire
        genre = request.POST.get('genre')
        age = request.POST.get('age')
        sleep_quality = float(request.POST.get('sleep_quality')) / 100.0  # Conversion en décimal
        heart_rate = request.POST.get('heart_rate')
        steps = request.POST.get('steps')
        sleep_duration = request.POST.get('sleep_duration')

        # Vérification des données
        print("Données reçues :")
        print("Genre:", genre)
        print("Âge:", age)
        print("Qualité du sommeil:", sleep_quality)
        print("Rythme cardiaque:", heart_rate)
        print("Étapes quotidiennes:", steps)
        print("Durée de sommeil:", sleep_duration)

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

        if result and user_prenom:
            # Connexion à MongoDB
            try:
                client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
                db = client[DATABASE_NAME]
                collection = db[COLLECTION_RESULTAT]

                # Insérer le résultat du test dans la collection MongoDB "resultat_test"
                result_data = {
                    'prenom': user_prenom,
                    'genre': genre,
                    'age': int(age),  # Assurez-vous que l'âge est un entier
                    'qualite_sommeil': sleep_quality * 100,  # Enregistrer en pourcentage
                    'rythme_cardiaque': float(heart_rate),  # Assurez-vous que c'est un float
                    'etapes_quotidiennes': int(steps),  # Assurez-vous que c'est un entier
                    'duree_sommeil': float(sleep_duration),  # Assurez-vous que c'est un float
                    'score': result.get('score', None),  # Enregistrer 'score' s'il est disponible
                    'prediction': result.get('response', None)  # Enregistrer 'response' s'il est disponible
                }
                # Vérifier les données avant l'insertion
                print("Données à insérer dans MongoDB:", result_data)
                
                collection.insert_one(result_data)
                print("Résultat enregistré avec succès dans MongoDB.")
            except Exception as e:
                print(f"Erreur lors de la connexion à MongoDB : {e}")

    return render(request, 'test.html', {
        'result': result, 
        'score': result['score'] if result else None, 
        'response': result['response'] if result else None
    })





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


from django.shortcuts import render, redirect
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Connexion à MongoDB
client = MongoClient('mongodb://root:pass12345@localhost:27017/')
db = client['connexion']
collection = db['patient']

def inscription(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        prenom = request.POST.get('prenom')
        mot_de_passe = request.POST.get('mot_de_passe')
        email = request.POST.get('email')
        
        # Créer le document patient à insérer dans MongoDB
        patient_data = {
            "prenom": prenom,
            "mot_de_passe": mot_de_passe,
            "email": email
        }
        
        # Insertion du document dans la collection 'patient'
        result = collection.insert_one(patient_data)
        
        # Vérification de l'insertion
        print(f"Document inséré avec l'ID: {result.inserted_id}")
        
        # Redirection après l'inscription réussie
        return redirect('inscription_reussie')
    
    # Afficher le formulaire si la requête n'est pas en POST
    return render(request, 'inscription.html')

def inscription_reussie(request):
    return render(request, 'inscription_reussie.html')

def directeur_reussi(request):
    # Vous pouvez passer des informations au template si nécessaire
    context = {
        'message': 'Connexion réussie en tant que directeur !'
    }
    return render(request, 'directeur_reussi.html', context)