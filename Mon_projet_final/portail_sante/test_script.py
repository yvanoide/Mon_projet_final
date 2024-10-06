from pymongo import MongoClient

def get_prediction_from_api(data):
    # Simuler la prédiction, remplace par l'appel API si nécessaire
    return {
        'score': 85,  # Exemple de score
        'response': 'Bon sommeil'  # Exemple de réponse
    }

def main():
    # Configuration de MongoDB
    MONGO_URI = 'mongodb://root:pass12345@localhost:27017/'
    DATABASE_NAME = 'connexion'
    COLLECTION_RESULTAT = 'resultat_test'

    # Saisir les données utilisateur
    user_prenom = input("Entrez le prénom de l'utilisateur : ")
    genre = input("Entrez le genre (Homme/Femme) : ")
    age = int(input("Entrez l'âge : "))
    sleep_quality = float(input("Entrez la qualité du sommeil (en pourcentage) : "))
    heart_rate = int(input("Entrez le rythme cardiaque : "))
    steps = int(input("Entrez le nombre d'étapes quotidiennes : "))
    sleep_duration = int(input("Entrez la durée de sommeil (en heures) : "))

    # Préparer les données
    data = {
        'genre': genre,
        'age': age,
        'sleep_quality': sleep_quality / 100.0,  # Conversion en décimal
        'heart_rate': heart_rate,
        'steps': steps,
        'sleep_duration': sleep_duration
    }

    # Obtenir la prédiction
    result = get_prediction_from_api(data)

    if result and user_prenom:
        # Connexion à MongoDB
        try:
            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            db = client[DATABASE_NAME]
            collection = db[COLLECTION_RESULTAT]

            # Insérer le résultat dans MongoDB
            result_data = {
                'prenom': user_prenom,
                'genre': genre,
                'age': age,
                'qualite_sommeil': sleep_quality,  # Reste en pourcentage
                'rythme_cardiaque': heart_rate,
                'etapes_quotidiennes': steps,
                'duree_sommeil': sleep_duration,
                'score': result.get('score', None),
                'prediction': result.get('response', None)
            }
            collection.insert_one(result_data)
            print("Résultat enregistré avec succès dans MongoDB.")
        except Exception as e:
            print(f"Erreur lors de la connexion à MongoDB : {e}")

if __name__ == '__main__':
    main()
