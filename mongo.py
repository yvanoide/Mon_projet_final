from pymongo import MongoClient

# Configurer les paramètres de connexion MongoDB
MONGO_URI = 'mongodb://root:pass12345@localhost:27017/'
DATABASE_NAME = 'connexion'
COLLECTION_NAME = 'patient'

# Connexion à MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Exemples de données à insérer
exemples_patient = [
    {"prenom": "Alice", "mot_de_passe": "alice123", "email": "alice@example.com"},
    {"prenom": "Bob", "mot_de_passe": "bob123", "email": "bob@example.com"},
    {"prenom": "Charlie", "mot_de_passe": "charlie123", "email": "charlie@example.com"},
    {"prenom": "Marie", "mot_de_passe": "habilité17", "email": "david@example.com"},
    {"prenom": "dede", "mot_de_passe": "dede", "email": "dede@example.com"}
]

# Insérer les exemples dans la collection MongoDB
collection.insert_many(exemples_patient)

print("Données insérées avec succès dans MongoDB.")
