import unittest
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

class TestModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialisation du dataset et des variables pour les tests."""
        # Charger le dataset
        cls.data = pd.read_csv('/home/yves/iadev-python/c-mlflow/Combine_Dataset_avec_score copy 2.csv')
        
        # Conversion de la colonne 'Genre' en valeurs numériques
        cls.data['Genre'] = cls.data['Genre'].map({'Male': 0, 'Female': 1})

        # Prétraitement des données (Vérification du type de la colonne 'Qualité du sommeil')
        if cls.data['Qualité du sommeil'].dtype != 'object':
            cls.data['Qualité du sommeil'] = cls.data['Qualité du sommeil'].astype(str)
        
        # Conversion des pourcentages (comme 'Qualité du sommeil') en décimales
        cls.data['Qualité du sommeil'] = cls.data['Qualité du sommeil'].str.rstrip('%').astype('float') / 100.0

        # Séparation des features et de la cible
        cls.X = cls.data.drop('Score de santé', axis=1)
        cls.y = cls.data['Score de santé']

        # Division des données (75% train, 25% test)
        cls.X_train, cls.X_test, cls.y_train, cls.y_test = train_test_split(cls.X, cls.y, test_size=0.25, random_state=42)

    def test_data_preprocessing(self):
        """Test si les données sont correctement prétraitées"""
        # Vérifier la conversion du genre
        self.assertTrue(self.data['Genre'].isin([0, 1]).all(), "Les valeurs dans 'Genre' doivent être 0 ou 1.")

        # Vérifier la conversion de 'Qualité du sommeil' en décimales
        self.assertTrue((self.data['Qualité du sommeil'] <= 1.0).all(), "Les pourcentages doivent être convertis en décimales")

    def test_model_training(self):
        """Test du modèle d'entraînement avec RandomForest et des métriques"""
        model = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42)

        # Enregistrer dans MLflow
        mlflow.start_run()

        try:
            # Entraîner le modèle
            model.fit(self.X_train, self.y_train)

            # Prédire sur l'ensemble de test
            predictions = model.predict(self.X_test)

            # Calculer les métriques
            mse = mean_squared_error(self.y_test, predictions)
            mae = mean_absolute_error(self.y_test, predictions)
            rmse = np.sqrt(mse)
            r2 = r2_score(self.y_test, predictions)

            # Vérifications des métriques
            self.assertGreater(r2, 0.5, "Le modèle doit avoir un score R² supérieur à 0.5")
            self.assertLess(rmse, 10, "Le RMSE doit être inférieur à 10")

            # Enregistrer le modèle et les métriques dans MLflow
            mlflow.sklearn.log_model(model, "model")
            mlflow.log_param("model_type", "RandomForestRegressor")
            mlflow.log_param("n_estimators", 200)
            mlflow.log_param("max_depth", 10)
            mlflow.log_metric("mse", mse)
            mlflow.log_metric("mae", mae)
            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("r2_score", r2)

            print(f'MSE: {mse:.4f}, MAE: {mae:.4f}, RMSE: {rmse:.4f}, R²: {r2:.4f}')

        finally:
            mlflow.end_run()

if __name__ == '__main__':
    unittest.main()
