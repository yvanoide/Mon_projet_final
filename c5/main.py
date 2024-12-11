from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import mysql.connector
import os

app = FastAPI()

# Configuration de la sécurité
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Modèle de données
class DataSante(BaseModel):
    id: Optional[int] = None
    Genre: Optional[str] = None
    Age: Optional[int] = None
    Qualite_sommeil: Optional[float] = None
    Rythme_cardiaque: Optional[float] = None
    Etapes_quotidiennes: Optional[int] = None
    Duree_sommeil: Optional[float] = None
    Score_sante: Optional[float] = None

# Utilisateur de modèle pour la sécurité
class User(BaseModel):
    username: str

# Fonction de connexion à la base de données
def get_database_connection():
    return mysql.connector.connect(
        host=os.getenv('DATABASE_HOST', 'localhost'),
        port=os.getenv('DATABASE_PORT', 3307),
        user=os.getenv('DATABASE_USER', 'traducteur'),
        password=os.getenv('DATABASE_PASSWORD', 'traducteur'),
        database=os.getenv('DATABASE_NAME', 'cquatres')
    )

# Simuler un utilisateur et un mot de passe pour l'exemple
def authenticate_user(username: str, password: str):
    # Simuler l'authentification ici
    return username == "user" and password == "password"

# Endpoint pour obtenir un token
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not authenticate_user(form_data.username, form_data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": "fake-token", "token_type": "bearer"}

# Fonction pour obtenir l'utilisateur courant
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Validation du token (simulée)
    if token != "fake-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return User(username="example")

# Récupérer une entrée par ID
@app.get("/data_sante/{id}", response_model=DataSante)
def read_data_sante(id: int, user: User = Depends(get_current_user)):
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM data_sante WHERE id = %s", (id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result is None:
        raise HTTPException(status_code=404, detail="Data not found")

    return result

# Récupérer toutes les entrées
@app.get("/data_sante/", response_model=List[DataSante])
def read_all_data_sante(user: User = Depends(get_current_user)):
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM data_sante")
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return result

# Créer une nouvelle entrée
@app.post("/data_sante/", response_model=DataSante)
def create_data_sante(data: DataSante, user: User = Depends(get_current_user)):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO data_sante (Genre, Age, Qualite_sommeil, Rythme_cardiaque, Etapes_quotidiennes, Duree_sommeil, Score_sante) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (data.Genre, data.Age, data.Qualite_sommeil, data.Rythme_cardiaque, data.Etapes_quotidiennes, data.Duree_sommeil, data.Score_sante)
    )
    conn.commit()
    data.id = cursor.lastrowid
    cursor.close()
    conn.close()

    return data

# Mettre à jour une entrée existante
@app.put("/data_sante/{id}", response_model=DataSante)
def update_data_sante(id: int, data: DataSante, user: User = Depends(get_current_user)):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE data_sante SET Genre = %s, Age = %s, Qualite_sommeil = %s, Rythme_cardiaque = %s, Etapes_quotidiennes = %s, Duree_sommeil = %s, Score_sante = %s WHERE id = %s",
        (data.Genre, data.Age, data.Qualite_sommeil, data.Rythme_cardiaque, data.Etapes_quotidiennes, data.Duree_sommeil, data.Score_sante, id)
    )
    conn.commit()
    cursor.close()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Data not found")

    data.id = id
    return data

# Supprimer une entrée
@app.delete("/data_sante/{id}", status_code=204)
def delete_data_sante(id: int, user: User = Depends(get_current_user)):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM data_sante WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Data not found")

    return
