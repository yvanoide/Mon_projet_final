import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import mlflow
import mlflow.sklearn

# Charger les données
data = pd.read_csv('/home/yves/iadev-python/c-mlflow/Combine_Dataset_avec_score copy 2.csv')

# Supposons que votre cible est dans la colonne 'target' et que les autres colonnes sont des caractéristiques
X = data.drop(columns=['Rythme cardiaque'])
y = data['Rythme cardiaque']

# Encoder les colonnes catégoriques
X = pd.get_dummies(X, drop_first=True)  # Encodage One-Hot

# Diviser les données
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Configurer MLflow
mlflow.start_run()

# Entraîner le modèle
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Prédire et évaluer
predictions = model.predict(X_test)
report = classification_report(y_test, predictions)
print(report)

# Enregistrer le modèle
mlflow.sklearn.log_model(model, "model")

# Ajouter des paramètres et des métriques
mlflow.log_param("description", "Ce modèle prédit la classe cible en utilisant un classificateur Random Forest.")
mlflow.log_param("model_type", "RandomForest")
mlflow.log_metric("accuracy", (predictions == y_test).mean())  # Exemple de métrique

# Terminer l'exécution
mlflow.end_run()
