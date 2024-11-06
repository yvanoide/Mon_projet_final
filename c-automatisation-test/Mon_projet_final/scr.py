import os

# Définir les variables d'environnement
os.environ['KAGGLE_USERNAME'] = 'yvespaulito'
os.environ['KAGGLE_KEY'] = '63e95328af24675ff1902fa4362480a9'

from kaggle.api.kaggle_api_extended import KaggleApi

# Créer une instance de l'API Kaggle
api = KaggleApi()

# Authentifier l'API Kaggle en utilisant les variables d'environnement
api.authenticate()

# Télécharger le jeu de données spécifié
dataset_slug = "mkechinov/eeg-sleep-analysis-dataset"  # Remplacer par le bon nom de jeu de données
api.dataset_download_files(dataset_slug, path='.', unzip=True)

print("Le téléchargement du jeu de données est terminé.")
