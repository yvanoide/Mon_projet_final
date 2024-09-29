import logging
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import numpy as np

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_data(num_samples=1000, num_features=10):
    logger.info(f"Génération de {num_samples} échantillons de données...")
    # Génération de données aléatoires
    X = np.random.rand(num_samples, num_features)  # Caractéristiques aléatoires
    y = np.random.randint(0, 2, num_samples)  # Cible binaire aléatoire (0 ou 1)
    logger.info("Données générées avec succès.")
    return pd.DataFrame(X), pd.Series(y)

def preprocess_data(data):
    logger.info("Prétraitement des données...")
    # Exemple de traitement simple, à adapter selon ton cas
    try:
        # Remplacer les valeurs manquantes par la médiane (aucune valeur manquante dans ce cas, mais pour le cas général)
        data.fillna(data.median(), inplace=True)
        logger.info("Prétraitement terminé avec succès.")
        return data
    except Exception as e:
        logger.error(f"Erreur lors du prétraitement des données : {e}")
        raise

def train_model(X_train, y_train):
    logger.info("Entraînement du modèle...")
    try:
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X_train, y_train)
        logger.info("Modèle entraîné avec succès.")
        return model
    except Exception as e:
        logger.error(f"Erreur lors de l'entraînement du modèle : {e}")
        raise

def evaluate_model(model, X_test, y_test):
    logger.info("Évaluation du modèle...")
    try:
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        logger.info(f"Précision du modèle : {accuracy}")
        return accuracy
    except Exception as e:
        logger.error(f"Erreur lors de l'évaluation du modèle : {e}")
        raise

def main():
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("Modele RandomForest - Santé")

    # Démarrer un nouveau run dans MLflow
    with mlflow.start_run():
        try:
            # Générer des données aléatoires
            X, y = generate_data(num_samples=1000, num_features=10)

            # Division des données en train/test
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Prétraitement
            X_train = preprocess_data(X_train)
            X_test = preprocess_data(X_test)

            # Entraînement du modèle
            model = train_model(X_train, y_train)

            # Évaluation du modèle
            accuracy = evaluate_model(model, X_test, y_test)

            # Enregistrement du modèle et des métriques dans MLflow
            logger.info("Enregistrement du modèle et des métriques dans MLflow...")
            mlflow.log_metric("accuracy", accuracy)
            mlflow.sklearn.log_model(model, "model")

        except Exception as e:
            logger.error(f"Erreur dans le processus principal : {e}")
            raise

if __name__ == "__main__":
    logger.info("Démarrage du script d'entraînement...")
    main()
    logger.info("Script terminé avec succès.")
