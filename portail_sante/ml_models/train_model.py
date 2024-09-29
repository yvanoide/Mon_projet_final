import mlflow
import mlflow.keras
import tensorflow as tf

# Définir un modèle simple
def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(100,)),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Simuler des données d'entraînement
def get_data():
    # Simulez des données aléatoires pour l'exemple
    import numpy as np
    data = np.random.random((1000, 100))
    labels = np.random.randint(2, size=(1000, 1))
    return data, labels

# Entraînement du modèle avec suivi MLflow
def train_model():
    data, labels = get_data()
    
    # Démarrer une session de suivi MLflow
    with mlflow.start_run():
        model = create_model()
        
        # Entraîner le modèle
        model.fit(data, labels, epochs=10, batch_size=32)
        
        # Enregistrer les métriques
        mlflow.log_param("epochs", 10)
        mlflow.log_param("batch_size", 32)
        
        # Enregistrer les métriques de performance
        mlflow.log_metric("accuracy", 0.95)  # Simuler une précision
        
        # Enregistrer le modèle avec MLflow
        mlflow.keras.log_model(model, "model")

if __name__ == "__main__":
    train_model()
