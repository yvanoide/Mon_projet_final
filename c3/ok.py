import pandas as pd
from sqlalchemy import create_engine
import os

# Variables de connexion
BDD_HOST = os.getenv('DATABASE_HOST', 'localhost')
BDD_PORT = os.getenv('DATABASE_PORT', 3307)
BDD_USER = os.getenv('DATABASE_USER', 'traducteur')
BDD_PASSWORD = os.getenv('DATABASE_PASSWORD', 'traducteur')
BDD_DATABASE = os.getenv('DATABASE_NAME', 'cquatres')

# Chemin vers le fichier CSV
csv_file_path = '/home/yves/iadev-python/c3/Combine_Dataset_avec_score.csv'

# Lire le fichier CSV avec pandas
df = pd.read_csv(csv_file_path)

# Afficher les noms de colonnes originaux pour vérification
print("Colonnes originales :")
print(df.columns)

# Renommer les colonnes pour correspondre aux noms de la table MySQL
df.rename(columns={
    'Genre': 'Genre',
    'Âge': 'Age',
    'Qualité du sommeil': 'Qualite_sommeil',
    'Rythme cardiaque': 'Rythme_cardiaque',
    'Étapes quotidiennes': 'Etapes_quotidiennes',
    'Durée du sommeil': 'Duree_sommeil',
    'Score de santé': 'Score_sante'
}, inplace=True)

# Vérifiez à nouveau les colonnes après renommage
print("Colonnes après renommage :")
print(df.columns)

# Convertir les pourcentages en décimales si nécessaire
def convert_percentage(value):
    if isinstance(value, str) and value.endswith('%'):
        return float(value.strip('%')) / 100
    return float(value)

# Appliquer la conversion sur 'Qualite_sommeil' si la colonne existe
if 'Qualite_sommeil' in df.columns:
    df['Qualite_sommeil'] = df['Qualite_sommeil'].apply(convert_percentage)
else:
    print("La colonne 'Qualite_sommeil' n'existe pas après renommage.")

# Vérifier les données après conversion
print("DataFrame preview après conversion :")
print(df.head())

# Créer une connexion à la base de données MySQL
connection_string = f"mysql+mysqlconnector://{BDD_USER}:{BDD_PASSWORD}@{BDD_HOST}:{BDD_PORT}/{BDD_DATABASE}"
engine = create_engine(connection_string)

# Insérer les données dans la table MySQL
df.to_sql('data_sante', con=engine, if_exists='append', index=False)

print("Données importées avec succès dans la table 'data_sante'.")
