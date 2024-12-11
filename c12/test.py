import unittest
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
import numpy as np

class TestModel(unittest.TestCase):
    def setUp(self):
        # Charger les données
        self.data = pd.read_csv('/home/yves/iadev-python/c12/Combine_Dataset_avec_score.csv')

        # Nettoyage des données : supprimer les '%' et convertir en valeurs décimales
        if 'Qualité du sommeil' in self.data.columns:
            self.data['Qualité du sommeil'] = self.data['Qualité du sommeil'].replace('%', '', regex=True).astype(float) / 100
        if 'Rythme cardiaque' in self.data.columns:
            self.data['Rythme cardiaque'] = pd.to_numeric(self.data['Rythme cardiaque'], errors='coerce')
        if 'Étapes quotidiennes' in self.data.columns:
            self.data['Étapes quotidiennes'] = pd.to_numeric(self.data['Étapes quotidiennes'], errors='coerce')
        if 'Durée du sommeil' in self.data.columns:
            self.data['Durée du sommeil'] = pd.to_numeric(self.data['Durée du sommeil'], errors='coerce')

        # Vérifier la taille des données et afficher un message d'erreur si nécessaire
        print(f"Nombre de lignes dans les données chargées: {len(self.data)}")

        # Préparation des données
        # Si le modèle s'attend à 7 caractéristiques, ajoutez les colonnes manquantes
        self.features = self.data[['Qualité du sommeil', 'Rythme cardiaque', 'Étapes quotidiennes', 'Durée du sommeil', 'Autre_feature_1', 'Autre_feature_2', 'Autre_feature_3']]
        self.target = self.data['Score de santé']

        # Diviser en données d'entraînement et de test
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.features, self.target, test_size=0.2, random_state=42)

        # Prétraitement
        self.scaler = StandardScaler()
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)

        # Charger le modèle sans optimiser l'optimiseur (si nécessaire)
        self.model = tf.keras.models.load_model('/home/yves/iadev-python/c12/best_model.keras', compile=False)
        self.model.compile(optimizer='adam', loss='mse', metrics=['mae'])

    def test_model_accuracy(self):
        # Tester le modèle sur les données de test
        loss, mae = self.model.evaluate(self.X_test_scaled, self.y_test)
        self.assertLess(mae, 10, "MAE is too high!")  # Exemple de test sur la performance

    def test_data_loading(self):
        # Tester le chargement des données
        # Adapter la taille attendue en fonction de la taille réelle des données
        self.assertEqual(len(self.data), 1294)  # Remplacer par la taille correcte des données si nécessaire

    def test_preprocessing(self):
        # Vérifier que les données sont bien prétraitées
        self.assertTrue(np.allclose(self.X_train_scaled.mean(axis=0), 0, atol=1e-7))  # Vérifier qu
