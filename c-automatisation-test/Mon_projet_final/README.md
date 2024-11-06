Portail de Santé pour la Détection des Troubles du Sommeil

Description
Ce projet est un portail de santé conçu pour assister les professionnels de santé dans l’évaluation du niveau de stress et la détection des troubles du sommeil des patients (comme l'insomnie et l'apnée du sommeil). Il combine une application web avec un système d'intelligence artificielle (IA) pour fournir des diagnostics basés sur des données de santé, facilitant la prise de décision pour les médecins et améliorant la gestion des patients.

L'IA intégrée analyse des paramètres tels que la durée et la qualité du sommeil, la fréquence cardiaque, la pression artérielle, et d'autres mesures importantes pour estimer les risques de troubles du sommeil.

Fonctionnalités Principales

1. Gestion des Utilisateurs
Patient : Les patients peuvent s’inscrire et se connecter pour accéder à un espace personnel. Ils peuvent réaliser des tests pour évaluer leur niveau de stress et leurs troubles du sommeil et consulter leurs résultats.
Administrateur (Infirmier) : Les administrateurs peuvent accéder à des données anonymisées des patients (sans noms ni âges) pour suivre l’évolution des résultats de tests. Ils assurent la gestion du portail et surveillent la base de données des patients.
Docteur (Directeur) : Les docteurs accèdent aux informations complètes des patients et peuvent interpréter les résultats fournis par l’IA pour affiner leurs diagnostics et adapter leurs traitements.

2. Évaluation du Niveau de Stress et des Troubles du Sommeil
Accès à un questionnaire personnalisé pour évaluer le niveau de stress des patients.
Génération de rapports détaillés basés sur les résultats du questionnaire et des prédictions de l'IA.

3. Intégration de l'Intelligence Artificielle
Utilisation de modèles de classification (SVM, arbres de décision, réseaux neuronaux) pour prédire le risque de troubles du sommeil et de stress.
Fonctionnalité de prédiction en temps réel : le modèle analyse les données des patients et génère un diagnostic.
Utilisation de MLflow pour surveiller les performances du modèle : suivi des métriques de qualité, latence, et fréquence des prédictions pour garantir la précision des résultats.

4. Sécurité et Authentification
Authentification avec JSON Web Token (JWT) pour sécuriser l’accès aux données.
Gestion des rôles et permissions : chaque utilisateur a un accès restreint selon son rôle (patient, administrateur, docteur).
Conformité aux recommandations de sécurité OWASP Top 10.

5. API RESTful
API construite avec FastAPI pour gérer les interactions entre le modèle de l'IA et l'application.
Endpoints pour :
Authentification et gestion des utilisateurs.

Prédiction des risques basés sur les données de santé.
Consultation et gestion des résultats.
Architecture Technique

Technologies Utilisées
Backend : Django pour la gestion des utilisateurs et des rôles, FastAPI pour exposer les endpoints d'intelligence artificielle.
Base de Données : MongoDB pour le stockage des données de santé et des profils utilisateurs.

Frontend : HTML/CSS avec des composants JavaScript pour l'interface utilisateur.
Machine Learning : Modèle de classification (SVM, arbre de décision, réseaux neuronaux) implémenté avec TensorFlow et sauvegardé en format .keras.
Surveillance et Suivi de Modèle : MLflow pour le suivi des métriques de performance et de la qualité du modèle.
Schéma de l'Architecture
Le portail repose sur une architecture RESTful où FastAPI gère les requêtes de prédiction et Django prend en charge l'application web et la gestion des utilisateurs. La base de données MongoDB stocke les informations des utilisateurs et les résultats des prédictions.

Diagramme de Cas d'Utilisation
Patient : Se connecte au portail, accède au test de stress, et consulte les résultats.
Administrateur : Se connecte pour visualiser les données anonymisées des patients.
Directeur (Docteur) : Se connecte pour accéder aux informations complètes des patients et interpréter les résultats.
Installation et Configuration
Prérequis
Python 3.8+
Django et FastAPI
MongoDB
TensorFlow pour le modèle d’IA
MLflow pour le suivi du modèle
Installation

Copier le code
git clone https://github.com/yvanoide/Mon_projet_final.git
cd Mon_projet_final

Installer les dépendances :

pip install -r requirements.txt
Lancer les serveurs :
Django : python manage.py runserver
FastAPI : uvicorn app.main:app --reload

Configuration
Assurez-vous que MongoDB est en cours d'exécution.
Configurez les fichiers d'environnement .env pour inclure les informations de connexion JWT et MongoDB.

Utilisation
Lancer l'application.
Créer un compte ou se connecter en tant que patient, administrateur ou docteur.

Effectuer un test de stress pour obtenir une évaluation et consulter les résultats.
Accéder aux fonctionnalités de l'IA pour obtenir un diagnostic automatique basé sur les données de santé.
Tests et Documentation

Tests unitaires : Utilisation de unittest pour tester les fonctionnalités de prédiction, de gestion des données, et d'authentification.
Documentation : Tous les endpoints et la configuration de l'API sont documentés avec Swagger, accessible via l’interface FastAPI.
