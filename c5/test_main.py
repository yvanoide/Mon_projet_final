import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app  # Assuming your FastAPI app is in main.py

client = TestClient(app)

@patch('main.get_database_connection')
def test_read_all_data_sante(mock_get_connection):
    # Mocking the cursor and connection
    mock_cursor = mock_get_connection.return_value.cursor.return_value
    mock_cursor.fetchall.return_value = [
        {"id": 1, "Genre": "Male", "Age": 30, "Qualite_sommeil": 7.5, "Rythme_cardiaque": 70.0,
         "Etapes_quotidiennes": 10000, "Duree_sommeil": 8.0, "Score_sante": 80.0}
    ]
    
    response = client.get("/data_sante/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["Genre"] == "Male"
