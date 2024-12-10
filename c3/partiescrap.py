import requests

def download_file(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Le fichier a été téléchargé avec succès sous {save_path}")
    else:
        print(f"Erreur {response.status_code} lors du téléchargement du fichier")

# URL directe vers le fichier "Time Americans Spend Sleeping.xlsx"
url = "https://data.world/makeovermonday/2019w23/Time Americans Spend Sleeping.xlsx"

# Chemin où sauvegarder le fichier localement
save_path = "Time Americans Spend Sleeping.xlsx"

# Appel de la fonction pour télécharger le fichier
download_file(url, save_path)
