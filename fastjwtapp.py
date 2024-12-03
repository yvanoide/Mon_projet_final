from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from datetime import datetime, timedelta

# Configuration FastAPI
app = FastAPI()

# JWT Configuration
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Fonction pour créer un token d'accès
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Fonction pour vérifier le token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token invalide")

# Fonction pour obtenir l'utilisateur actuel à partir du token
def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "user" and form_data.password == "password":
        access_token = create_access_token(
            data={"sub": form_data.username},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Identifiants invalides")

# Route protégée /agenda
@app.get("/agenda")
async def agenda(current_user: dict = Depends(get_current_user)):
    return {"message": "Bienvenue sur l'agenda, vous êtes connecté!"}

# Route protégée /test
@app.get("/test")
async def test(current_user: dict = Depends(get_current_user)):
    return {"message": "Bienvenue sur la page de test, vous êtes connecté!"}

# Route protégée /connexion_reussi
@app.get("/connexion_reussi")
async def connexion_reussi(current_user: dict = Depends(get_current_user)):
    return {"message": "Connexion réussie, vous êtes maintenant connecté!"}

# Route de connexion
@app.get("/connexion")
async def connexion(request: Request):
    return {"message": "Page de connexion, entrez vos informations!"}

# Rediriger les pages protégées en cas d'accès non autorisé
@app.get("/agenda_protege")
async def agenda_protege(current_user: dict = Depends(get_current_user)):
    return {"message": "Vous avez accédé à la page Agenda protégée."}

@app.get("/test_protege")
async def test_protege(current_user: dict = Depends(get_current_user)):
    return {"message": "Vous avez accédé à la page Test protégée."}

@app.get("/connexion_reussi_protege")
async def connexion_reussi_protege(current_user: dict = Depends(get_current_user)):
    return {"message": "Vous avez accédé à la page Connexion Réussie protégée."}

