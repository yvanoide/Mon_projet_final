from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient('mongodb://root:pass12345@localhost:27017/')
db = client['data']
collection = db['enorme_anonyme']

# Récupérer les données depuis MongoDB
patient_data = list(collection.find())

# Affichage des données
for patient in patient_data:
    # Renommer _id en id pour l'affichage
    patient_id = str(patient.pop('_id'))  # Convertir l'ObjectId en chaîne pour l'afficher
    # Récupérer les autres champs
    qualite_du_sommeil = patient.get('Qualité du sommeil', 'N/A')
    rythme_cardiaque = patient.get('Rythme cardiaque', 'N/A')
    etapes_quotidiennes = patient.get('Étapes quotidiennes', 'N/A')
    duree_du_sommeil = patient.get('Durée du sommeil', 'N/A')
    score_de_sante = patient.get('Score de santé', 'N/A')

    # Afficher les informations du patient
    print(f"ID: {patient_id}, Qualité du sommeil: {qualite_du_sommeil}, "
          f"Rythme cardiaque: {rythme_cardiaque}, Étapes quotidiennes: {etapes_quotidiennes}, "
          f"Durée du sommeil: {duree_du_sommeil}, Score de santé: {score_de_sante}")
