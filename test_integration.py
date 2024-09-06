import pytest
import requests

BASE_URL = 'http://127.0.0.1:8002'  # URL de votre API FastAPI

def test_login():
    url = f'{BASE_URL}/token'
    payload = {
        'username': 'user',
        'password': 'password'
    }
    response = requests.post(url, data=payload)
    assert response.status_code == 200
    assert 'access_token' in response.json()

def test_predict():
    # Obtenir un jeton d'accès
    login_url = f'{BASE_URL}/token'
    payload = {
        'username': 'user',
        'password': 'password'
    }
    response = requests.post(login_url, data=payload)
    assert response.status_code == 200
    access_token = response.json()['access_token']

    # Utiliser le jeton pour faire une prédiction
    predict_url = f'{BASE_URL}/predict'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    predict_data = {
        'genre': 'Male',
        'age': 45,
        'sleep_quality': 0.9,
        'heart_rate': 75,
        'steps': 10000,
        'sleep_duration': 4.5
    }
    response = requests.post(predict_url, json=predict_data, headers=headers)
    assert response.status_code == 200
    assert 'score' in response.json()
    assert 'response' in response.json()

def test_health_check():
    url = f'{BASE_URL}/health'
    response = requests.get(url)
    assert response.status_code == 200
    assert 'status' in response.json()
