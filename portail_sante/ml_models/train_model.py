import mlflow
import mlflow.tensorflow  # Si tu utilises TensorFlow pour ton modèle
import pandas as pd

# Configurer l'URI de tracking MLflow
mlflow.set_tracking_uri("http://localhost:5000")  # Change selon ton environnement


import mlflow
import mlflow.tensorflow
import pandas as pd
from tensorflow import keras

# Charger les données du patient
data = pd.read_csv('/home/yves/iadev-python/c13/Mon_projet_fina/Combine_Dataset_avec_score.csv')

# Supposons que la dernière colonne est la cible et le reste sont les features
X = data.iloc[:, :-1]  # Toutes les colonnes sauf la dernière
y = data.iloc[:, -1]   # La dernière colonne

# Commencer une nouvelle exécution MLflow
with mlflow.start_run():
    # Définir le modèle
    model = keras.Sequential([
        keras.layers.Dense(64, activation='relu', input_shape=(X.shape[1],)),
        keras.layers.Dense(1)  # Adapté pour une sortie de régression
    ])

    # Compiler le modèle
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Entraîner le modèle
    model.fit(X, y, epochs=10)

    # Enregistrer le modèle avec MLflow
    mlflow.tensorflow.log_model(model, "model")

    # Enregistrer les paramètres et métriques
    mlflow.log_param("epochs", 10)
    mlflow.log_metric("loss", model.evaluate(X, y))
