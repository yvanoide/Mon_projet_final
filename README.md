# Documentation du Projet d'IA

## Introduction

Ce document couvre la procédure d'installation de l'environnement de test, les dépendances installées, ainsi que la procédure d'exécution des tests et de calcul de la couverture. Il fournit également des détails sur les cas de test définis et les outils utilisés.

## 1. Procédure d'Installation de l'Environnement de Test

### 1.1 Configuration de l'Environnement dans Google Colab

Pour configurer l'environnement de test dans Google Colab, suivez les étapes ci-dessous :

1. **Ouvrir Google Colab** : Créez un nouveau notebook ou ouvrez un notebook existant.

2. **Installation des Dépendances** :
   Nous utilisons les bibliothèques suivantes :
   ```python
   !pip install tensorflow joblib pandas

Téléchargement des Fichiers : Téléchargez les fichiers nécessaires depuis Google Drive :
python
Copier le code
from google.colab import drive
drive.mount('/content/drive')

import shutil
shutil.copy('/content/drive/MyDrive/Colab Notebooks/service ia.ipynb', '/content/service_ia.ipynb')
1.2 Fichiers Requis
Assurez-vous que les fichiers suivants sont disponibles dans l'environnement :

best_model.keras pour le modèle
target_scaler.joblib pour le scaler
Ces fichiers doivent être chargés correctement depuis Google Drive pour permettre l'évaluation et la prédiction.

2. Dépendances Installées
Les dépendances nécessaires pour ce projet sont :

TensorFlow : pour l'entraînement et l'évaluation du modèle.
Joblib : pour le chargement et la sauvegarde du scaler.
Pandas : pour la manipulation des données.
Unittest : pour la création et l'exécution des tests.
3. Procédure d'Exécution des Tests
Pour exécuter les tests, suivez ces étapes :

Exécution des Tests : Utilisez la commande suivante pour exécuter les tests :

python
Copier le code
!python -m unittest discover -s /content
Calcul de la Couverture des Tests : Installez coverage et générez un rapport de couverture :

python
Copier le code
!pip install coverage
!coverage run -m unittest discover -s /content
!coverage report
!coverage html
Téléchargez le rapport de couverture :

python
Copier le code
from google.colab import files
files.download('/content/htmlcov/index.html')
4. Liste et Définition des Cas de Test
Les cas de test suivants ont été définis pour assurer la robustesse et la fiabilité du modèle :

Chargement des Données : Vérifie que les données sont correctement chargées depuis les fichiers.

Conversion des Pourcentages en Décimaux : Assure que les pourcentages sont correctement convertis en décimaux.

Normalisation des Caractéristiques et de la Cible : Vérifie que les caractéristiques et la cible sont normalisées correctement.

Division des Données (Train/Test Split) : Confirme que les ensembles d'entraînement et de test sont correctement séparés et que leurs tailles sont correctes.

Entraînement du Modèle : Vérifie que le modèle peut être entraîné sans générer d'erreurs.

Évaluation du Modèle : Assure que le modèle peut être évalué sans erreur sur les données de test.

Sauvegarde et Chargement du Modèle et des Scalers : Vérifie que le modèle et les scalers peuvent être sauvegardés et chargés correctement.

Prédiction avec des Nouvelles Données : Vérifie que le modèle peut faire des prédictions sur de nouvelles données sans erreur.

5. Outils de Test
Framework de Test : Nous avons utilisé unittest, un module intégré de Python, adapté à notre environnement technique basé sur Python et TensorFlow.
Bibliothèques : Les bibliothèques utilisées incluent TensorFlow pour le modèle, Joblib pour le scaler, et Pandas pour la manipulation des données.
Accessibilité
La documentation a été rédigée en suivant les recommandations d’accessibilité, y compris :

Structure du Document : Titres clairs et table des matières.
Contraste Suffisant : Texte avec contraste suffisant par rapport à l'arrière-plan.
Texte Alternatif pour les Images : Descriptions textuelles pour les images et graphiques.
Langage Simple et Lisibilité : Langage clair et paragraphes courts.
Nous nous assurons que le document est accessible et conforme aux normes d'accessibilité pour garantir une utilisation facile par tous les utilisateurs.

Conclusion
Tous les tests ont été exécutés avec succès, sauf une erreur signalée qui a été corrigée. Les outils et bibliothèques utilisés sont cohérents avec l'environnement technique du projet, garantissant la robustesse et la fiabilité des tests avant le déploiement du modèle.

Pour toute question ou assistance, veuillez nous contacter via les informations de contact fournies dans le dépôt.
