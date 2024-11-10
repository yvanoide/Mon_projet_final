import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import mlflow
import mlflow.sklearn

# Charger les données
data = pd.read_csv('/home/yves/iadev-python/c-mlflow/Combine_Dataset_avec_score copy 2.csv')

# Préparer les données
X = data.drop(columns=['Étapes quotidiennes'])  # Remplacez 'target' par votre nom de colonne cible
y = data['Étapes quotidiennes']

# Encoder les colonnes catégoriques
X = pd.get_dummies(X, drop_first=True)

# Diviser les données
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Configurer MLflow
mlflow.start_run()

# Entraîner le modèle
model = RandomForestClassifier(n_estimators=100, max_depth=10)  # Ajoutez vos hyperparamètres ici
model.fit(X_train, y_train)

# Prédire et évaluer
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
report = classification_report(y_test, predictions)

# Enregistrer le modèle
mlflow.sklearn.log_model(model, "model")

# Ajouter des paramètres
mlflow.log_param("model_type", "RandomForest")
mlflow.log_param("n_estimators", 100)
mlflow.log_param("max_depth", 10)

# Ajouter des métriques
mlflow.log_metric("accuracy", accuracy)

# Logger le rapport de classification en tant qu'artéfact
with open("classification_report.txt", "w") as f:
    f.write(report)
mlflow.log_artifact("classification_report.txt")

# Ajouter une description
mlflow.set_tag("description", "Ce modèle prédit la classe cible en utilisant un classificateur Random Forest avec des hyperparamètres ajustés.")

# Terminer l'exécution
mlflow.end_run()
