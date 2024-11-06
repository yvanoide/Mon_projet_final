import os
from fastapi.testclient import TestClient
import pytest
from main import app  # Make sure to import your FastAPI app

# Set up a TestClient for your FastAPI app
client = TestClient(app)

# Simulated environment variables for the test
os.environ['DATABASE_HOST'] = 'localhost'
os.environ['DATABASE_PORT'] = '3307'
os.environ['DATABASE_USER'] = 'traducteur'
os.environ['DATABASE_PASSWORD'] = 'traducteur'
os.environ['DATABASE_NAME'] = 'traducteur'

# Helper function to get a token
def get_access_token(username: str = "user", password: str = "password"):
    response = client.post("/token", data={"username": username, "password": password})
    return response.json().get("access_token")

# Test for token generation
def test_login():
    response = client.post("/token", data={"username": "user", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()

# Test for getting all health data
def test_read_all_data_sante():
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/data_sante/", headers=headers)
    assert response.status_code == 200

# Test for creating a new health data entry
def test_create_data_sante():
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "Genre": "Femme",
        "Age": 30,
        "Qualite_sommeil": 8.0,
        "Rythme_cardiaque": 70.0,
        "Etapes_quotidiennes": 10000,
        "Duree_sommeil": 7.5,
        "Score_sante": 90.0
    }
    response = client.post("/data_sante/", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json()["Genre"] == data["Genre"]

# Test for reading a specific health data entry
def test_read_data_sante():
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # First, create an entry to read it
    create_response = client.post("/data_sante/", json={
        "Genre": "Homme",
        "Age": 25,
        "Qualite_sommeil": 6.5,
        "Rythme_cardiaque": 75.0,
        "Etapes_quotidiennes": 8000,
        "Duree_sommeil": 6.0,
        "Score_sante": 80.0
    }, headers=headers)

    entry_id = create_response.json()["id"]

    # Now read the entry
    response = client.get(f"/data_sante/{entry_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == entry_id

# Test for updating a health data entry
def test_update_data_sante():
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # First, create an entry to update it
    create_response = client.post("/data_sante/", json={
        "Genre": "Femme",
        "Age": 40,
        "Qualite_sommeil": 7.0,
        "Rythme_cardiaque": 65.0,
        "Etapes_quotidiennes": 12000,
        "Duree_sommeil": 8.0,
        "Score_sante": 85.0
    }, headers=headers)

    entry_id = create_response.json()["id"]
    
    # Update the entry
    updated_data = {
        "Genre": "Femme",
        "Age": 41,
        "Qualite_sommeil": 8.0,
        "Rythme_cardiaque": 70.0,
        "Etapes_quotidiennes": 13000,
        "Duree_sommeil": 7.5,
        "Score_sante": 88.0
    }
    response = client.put(f"/data_sante/{entry_id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["Age"] == updated_data["Age"]

# Test for deleting a health data entry
def test_delete_data_sante():
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # First, create an entry to delete it
    create_response = client.post("/data_sante/", json={
        "Genre": "Homme",
        "Age": 50,
        "Qualite_sommeil": 5.0,
        "Rythme_cardiaque": 80.0,
        "Etapes_quotidiennes": 5000,
        "Duree_sommeil": 5.0,
        "Score_sante": 75.0
    }, headers=headers)

    entry_id = create_response.json()["id"]
    
    # Now delete the entry
    response = client.delete(f"/data_sante/{entry_id}", headers=headers)
    assert response.status_code == 204

    # Try to read the deleted entry to ensure it's gone
    response = client.get(f"/data_sante/{entry_id}", headers=headers)
    assert response.status_code == 404
