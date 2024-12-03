from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import jwt
import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# MongoDB Configuration
MONGO_URI = "mongodb://root:pass12345@localhost:27017/"
client = MongoClient(MONGO_URI)
db = client["connexion"]
patients = db["patient"]

# Token secret and expiration time
SECRET_KEY = "votre_clé_secrète"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 30

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet toutes les origines
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Permet tous les en-têtes
)

# Pydantic model for login
class UserLogin(BaseModel):
    prenom: str
    mot_de_passe: str

# Token generation function
def create_access_token(prenom: str):
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=EXPIRE_MINUTES)
    to_encode = {"sub": prenom, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/login")
async def login(user: UserLogin):
    patient = patients.find_one({"prenom": user.prenom})
    if not patient or patient["mot_de_passe"] != user.mot_de_passe:
        raise HTTPException(status_code=401, detail="Prénom ou mot de passe incorrect")
    
    access_token = create_access_token(user.prenom)
    # Renvoi d'un token JWT et d'un signal de succès
    return {"access_token": access_token, "token_type": "bearer", "status": "success"}

# Charger les templates
templates = Jinja2Templates(directory="path/to/templates")

@app.get("/connexion_reussie", response_class=HTMLResponse)
async def connexion_reussie(request: Request):
    return templates.TemplateResponse("connexion_reussie.html", {"request": request})


