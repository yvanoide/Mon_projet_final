import pandas as pd

# Chemin vers le fichier CSV d'origine
input_file_path = '/home/yves/iadev-python/c3/csv/Sleep_health_and_lifestyle_dataset.csv'

# Chemin vers le fichier CSV de sortie
output_file_path = '/home/yves/iadev-python/c3/csv/bigdata.csv'

# Lire le fichier CSV d'origine
data = pd.read_csv(input_file_path)

# Dupliquer les données 20 fois
duplicated_data = pd.concat([data] * 700, ignore_index=True)

# Sauvegarder le résultat dans un nouveau fichier CSV
duplicated_data.to_csv(output_file_path, index=False)

print(f"Les données ont été dupliquées et sauvegardées dans {output_file_path}")
