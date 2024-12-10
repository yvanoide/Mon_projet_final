import zipfile
import os

# Chemin du fichier ZIP et du dossier de destination
zip_file_path = '/home/yves/iadev-python/c3/dataset.zip'
extract_folder = '/home/yves/iadev-python/c3/dataset_extracted/'

# Vérifier si le fichier ZIP existe
if os.path.isfile(zip_file_path):
    # Décompresser le fichier ZIP
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # Extraire le contenu dans le dossier spécifié
        zip_ref.extractall(extract_folder)
        print(f"Le fichier ZIP a été décompressé avec succès dans {extract_folder}.")
else:
    print(f"Le fichier ZIP n'existe pas à l'emplacement spécifié : {zip_file_path}")
