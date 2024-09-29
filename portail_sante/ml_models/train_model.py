import mlflow
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import joblib
import tensorflow as tf
import os

# Définir l'URI de tracking pour MLflow
mlflow.set_tracking_uri("http://127.0.0.1:5000")

# Vérifier la connexion à MLflow
try:
    mlflow.get_tracking_uri()  # Vérifier si l'URI est correcte
    print("Connexion à MLflow réussie.")
except Exception as e:
    print(f"Erreur de connexion à MLflow: {e}")

# Essayer de charger les données depuis une URL
url = 'https://example.com/Combine_Dataset_avec_score.csv'  # Assurez-vous que cette URL est correcte
local_file = '/tmp/test_data.csv'  # Utiliser un fichier local comme alternative

try:
    if os.path.exists(local_file):
        data = pd.read_csv(local_file)  # Charger depuis le fichier local
        print(f"Fichier local chargé : {local_file}")
    else:
        data = pd.read_csv(url)  # Charger depuis l'URL
        print(f"Données chargées depuis l'URL : {url}")
except Exception as e:
    print(f"Erreur lors du chargement des données : {e}")
    exit(1)

# Continuez avec le reste de votre code...
