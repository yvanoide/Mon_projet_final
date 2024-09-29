import mlflow
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import joblib
import tensorflow as tf

# Définir l'URI de tracking pour MLflow
mlflow.set_tracking_uri("http://127.0.0.1:5000")

# Vérifier la connexion à MLflow
try:
    mlflow.get_tracking_uri()  # Vérifier si l'URI est correcte
    print("Connexion à MLflow réussie.")
except Exception as e:
    print(f"Erreur de connexion à MLflow: {e}")

# Chemin vers le fichier CSV (ajuste le chemin ici)
file_path = '/home/yves/iadev-python/c13/Combine_Dataset_avec_score.csv'  # Assure-toi que ce chemin est correct

# Charger les données depuis le fichier CSV
try:
    data = pd.read_csv(file_path)
except FileNotFoundError as e:
    print(f"Erreur lors du chargement du fichier CSV : {e}")
    exit(1)

# Continue avec le reste de ton code...

# 4. Convertir les pourcentages en décimaux
def convertir_pourcentage_en_decimal(pourcentage):
    if isinstance(pourcentage, str) and '%' in pourcentage:
        return float(pourcentage.replace('%', '')) / 100.0
    return float(pourcentage)

data['Qualité du sommeil'] = data['Qualité du sommeil'].apply(convertir_pourcentage_en_decimal)

# 5. Sélectionner les caractéristiques et la cible
features = data[['Qualité du sommeil', 'Rythme cardiaque', 'Étapes quotidiennes', 'Durée du sommeil']]
target = data['Score de santé']

# 6. Normaliser la cible
target_scaler = MinMaxScaler()
target = target_scaler.fit_transform(target.values.reshape(-1, 1))

# 7. Diviser les données en ensemble d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# 8. Prétraiter les données
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 9. Sauvegarder le scaler
scaler_path = '/home/yves/iadev-python/c13/scaler.joblib'
joblib.dump(scaler, scaler_path)

# 10. Sauvegarder le scaler pour la cible
target_scaler_path = '/home/yves/iadev-python/c13/preprocessor.joblib'
joblib.dump(target_scaler, target_scaler_path)

# 11. Définir le modèle de réseau de neurones
model = tf.keras.models.Sequential([
    tf.keras.layers.InputLayer(input_shape=(X_train_scaled.shape[1],)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1)  # Pas de fonction d'activation pour la régression
])

# 12. Compiler le modèle
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# 13. Configurer TensorBoard comme callback
log_dir = "logs/"
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

# 14. Entraîner le modèle avec TensorBoard activé
history = model.fit(
    X_train_scaled,
    y_train,
    epochs=20,
    validation_split=0.2,
    verbose=1,
    callbacks=[tensorboard_callback]
)
