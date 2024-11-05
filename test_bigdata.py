import os
import pytest
import requests
from unittest.mock import patch, MagicMock
import pandas as pd

# Ajouter le chemin du dossier parent au sys.path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import bigdata  # Assurez-vous que bigdata est importé correctement

# Tests
def test_download_dataset():
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.iter_content = MagicMock(return_value=[b'test data'])

        bigdata.download_dataset()

        mock_get.assert_called_once()
        assert os.path.isfile(bigdata.ZIP_FILE_NAME)

def test_extract_zip():
    # Simulez la création d'un fichier zip pour le test
    with patch('zipfile.ZipFile') as mock_zip:
        mock_zip.return_value.__enter__.return_value.extractall = MagicMock()
        bigdata.extract_zip()
        mock_zip.assert_called_once_with(bigdata.ZIP_FILE_NAME, 'r')
        mock_zip.return_value.__enter__.return_value.extractall.assert_called_once_with(bigdata.EXTRACTED_FOLDER)

def test_read_csv():
    with patch('pandas.read_csv') as mock_read_csv:
        mock_read_csv.return_value = pd.DataFrame({'column1': [1, 2], 'column2': [3, 4]})
        
        df = bigdata.read_csv()
        assert df.shape == (2, 2)  # Vérifiez que le DataFrame a 2 lignes et 2 colonnes
        mock_read_csv.assert_called_once_with(os.path.join(bigdata.EXTRACTED_FOLDER, bigdata.CSV_FILE_NAME))

if __name__ == "__main__":
    pytest.main()
