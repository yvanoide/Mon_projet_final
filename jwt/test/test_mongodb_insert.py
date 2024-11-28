import pytest
from pymongo import MongoClient
import re

# Configurer les paramètres de connexion MongoDB
MONGO_URI = 'mongodb://root:pass12345@localhost:27017/'
DATABASE_NAME = 'connexion'
COLLECTION_NAME = 'patient'

# Connexion à MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Exemples de données à insérer (mise à jour des mots de passe)
exemples_patient = [
    {"prenom": "Alice", "mot_de_passe": "alice123", "email": "alice@example.com"},
    {"prenom": "Bob", "mot_de_passe": "bob123", "email": "bob@example.com"},
    {"prenom": "Charlie", "mot_de_passe": "charlie123", "email": "charlie@example.com"},
    {"prenom": "David", "mot_de_passe": "david123", "email": "david@example.com"},
    {"prenom": "Eve", "mot_de_passe": "eve123", "email": "eve@example.com"}
]

# Test d'insertion des exemples dans la collection MongoDB
@pytest.fixture(scope='module')
def insert_data():
    # Nettoyer la collection avant l'insertion
    collection.delete_many({})
    # Insérer les exemples dans la collection MongoDB
    collection.insert_many(exemples_patient)
    yield
    # Nettoyer la base de données après les tests
    collection.delete_many({})

def test_insertion_data(insert_data):
    # Vérifier que les données ont bien été insérées
    count = collection.count_documents({})
    assert count == 5, f"Expected 5 documents, but found {count}"

def test_data_content(insert_data):
    # Vérifier que les données insérées sont correctes
    documents = list(collection.find({}))
    inserted_names = [doc["prenom"] for doc in documents]
    expected_names = ["Alice", "Bob", "Charlie", "David", "Eve"]
    assert set(inserted_names) == set(expected_names), f"Expected names {expected_names}, but got {inserted_names}"

# Test de validité pour les emails
def test_valid_email_format(insert_data):
    documents = collection.find({})
    for doc in documents:
        email = doc["email"]
        # Vérifier que l'email a un format valide
        assert re.match(r"[^@]+@[^@]+\.[^@]+", email), f"Invalid email format: {email}"

# Test de validité pour les mots de passe
def test_valid_password(insert_data):
    documents = collection.find({})
    for doc in documents:
        password = doc["mot_de_passe"]
        # Vérifier que le mot de passe contient au moins 6 caractères
        assert len(password) >= 6, f"Password too short: {password}"
