import os
import requests
import pandas as pd
import zipfile

# Configuration
KAGGLE_USERNAME = 'yvespaulito'  
KAGGLE_KEY = '63e95328af24675ff1902fa4362480a9' 
DATASET_NAME = 'prasad22/healthcare-dataset'
ZIP_FILE_NAME = 'dataset.zip'
EXTRACTED_FOLDER = 'dataset'
CSV_FILE_NAME = 'healthcare_dataset.csv'  # Nom corrigé du fichier CSV

# Télécharger le dataset
def download_dataset():
    headers = {
        'Authorization': f'Bearer {KAGGLE_KEY}'
    }
    url = f'https://www.kaggle.com/api/v1/datasets/download/{DATASET_NAME}'
    response = requests.get(url, headers=headers, stream=True)

    if response.status_code == 200:
        with open(ZIP_FILE_NAME, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Dataset downloaded successfully.")
    else:
        print(f"Failed to download dataset. Status code: {response.status_code}")

# Extraire le fichier ZIP
def extract_zip():
    with zipfile.ZipFile(ZIP_FILE_NAME, 'r') as zip_ref:
        zip_ref.extractall(EXTRACTED_FOLDER)
        print("Dataset extracted successfully.")
        # Liste le contenu du fichier ZIP pour identifier le fichier CSV
        print("Files in ZIP:")
        zip_ref.printdir()

# Lire le fichier CSV
def read_csv():
    # Liste le contenu du dossier extrait pour identifier le fichier CSV
    print("Files in extracted folder:")
    for root, dirs, files in os.walk(EXTRACTED_FOLDER):
        for file in files:
            print(f"Found file: {file}")

    # Utilisation du nom correct du fichier CSV extrait
    file_path = os.path.join(EXTRACTED_FOLDER, CSV_FILE_NAME)
    
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    df = pd.read_csv(file_path)
    return df

# Exécution des fonctions
download_dataset()
extract_zip()
df = read_csv()
print(df.head())

#Le script semble fonctionner correctement maintenant. Voici un résumé de ce que fait le code :


#Le fichier ZIP contenant le dataset est téléchargé depuis Kaggle.

#Le contenu du ZIP est décompressé dans le dossier dataset.