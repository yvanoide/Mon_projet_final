import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score
)
import mlflow
import mlflow.sklearn

# Charger le dataset
data = pd.read_csv('/home/yves/iadev-python/c-mlflow/Combine_Dataset_avec_score copy 2.csv')

# Prétraitement des données
# Conversion de la colonne 'Genre' en valeurs numériques
data['Genre'] = data['Genre'].map({'Male': 0, 'Female': 1})

# Conversion des pourcentages (comme 'Qualité du sommeil') en décimales
data['Qualité du sommeil'] = data['Qualité du sommeil'].str.rstrip('%').astype('float') / 100.0

# S'assurer que toutes les colonnes numériques sont bien formatées
X = data.drop('Score de santé', axis=1)  # Features (toutes les colonnes sauf "Score de santé")
y = data['Score de santé']  # Target (la colonne "Score de santé")

# Diviser les données en ensembles d'entraînement et de test (75% train, 25% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Initialiser le modèle RandomForest pour la régression avec 200 arbres et max_depth de 10
model = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42)

# Enregistrer l'exécution dans MLflow
mlflow.start_run()

try:
    # Entraîner le modèle
    model.fit(X_train, y_train)

    # Prédire sur l'ensemble de test
    predictions = model.predict(X_test)

    # Calculer les métriques
    mse = mean_squared_error(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predictions)

    # Enregistrer le modèle dans MLflow
    mlflow.sklearn.log_model(model, "model")

    # Enregistrer des paramètres
    mlflow.log_param("model_type", "RandomForestRegressor")
    mlflow.log_param("n_estimators", 200)
    mlflow.log_param("max_depth", 10)

    # Enregistrer toutes les métriques
    mlflow.log_metric("mse", mse)
    mlflow.log_metric("mae", mae)
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2_score", r2)

    print(f'MSE: {mse:.4f}, MAE: {mae:.4f}, RMSE: {rmse:.4f}, R²: {r2:.4f}')

finally:
    # Terminer l'exécution de MLflow
    mlflow.end_run()
