import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
import mlflow
import mlflow.sklearn
from sklearn.preprocessing import LabelEncoder

# Charger les données
data = pd.read_csv('/home/yves/iadev-python/c-mlflow/Combine_Dataset_avec_score copy 2.csv')

# Assurez-vous que les colonnes suivantes existent dans vos données
# Pour cet exemple, nous supposons que 'label' est la colonne cible et que vous avez des caractéristiques numériques
features = data.drop(columns=['Rythme cardiaque'])
labels = data['Rythme cardiaque']

# Encodage des variables catégorielles
label_encoders = {}
for column in features.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    features[column] = le.fit_transform(features[column])
    label_encoders[column] = le

# Séparer les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Début de la session MLflow
mlflow.start_run()

try:
    # Créer et entraîner le modèle
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    # Évaluer le modèle
    predictions = model.predict(X_test)
    report = classification_report(y_test, predictions)

    # Enregistrer le modèle dans MLflow
    mlflow.sklearn.log_model(model, "decision_tree_model")
    
    # Enregistrer les métriques
    mlflow.log_param("model_type", "Decision Tree")
    mlflow.log_metric("accuracy", (predictions == y_test).mean())
    
    # Afficher le rapport de classification
    print(report)

except Exception as e:
    print("Une erreur est survenue :", e)

finally:
    mlflow.end_run()
