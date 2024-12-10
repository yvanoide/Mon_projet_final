from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from pymongo.errors import PyMongoError

# Utilisez `main` comme instance FastAPI principale
main = FastAPI()

# Configuration MongoDB
MONGO_URI = 'mongodb://root:pass12345@localhost:27017/'
DATABASE_NAME = 'data'
COLLECTION_NAME = 'bigdata'

# Connexion à la base MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Définition du modèle Pydantic pour les données de santé
class DataSante(BaseModel):
    # Définissez les champs du modèle ici, par exemple :
    genre: str
    age: int
    qualite_sommeil: float
    rythme_cardiaque: int
    etapes_quotidiennes: int
    duree_sommeil: float
    score_sante: float

@main.get("/")
async def root():
    return {"message": "Hello World"}

@main.get("/data/{id}")
async def get_data_by_id(id: str):
    try:
        object_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    document = collection.find_one({"_id": object_id})
    
    if document is None:
        raise HTTPException(status_code=404, detail="Data not found")
    
    document["_id"] = str(document["_id"])
    return document

@main.post("/data_sante/")
async def create_data(data: DataSante):
    try:
        data_dict = jsonable_encoder(data)
        result = collection.insert_one(data_dict)
        return {"_id": str(result.inserted_id), **data_dict}
    except PyMongoError:
        raise HTTPException(status_code=500, detail="Database error")

@main.put("/data_sante/{id}")
async def update_data(id: str, data: DataSante):
    try:
        updated_data = {k: v for k, v in data.dict().items() if v is not None}
        if updated_data:
            result = collection.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
            if result.modified_count:
                return {"_id": id, **updated_data}
            raise HTTPException(status_code=404, detail="Data not found")
        raise HTTPException(status_code=400, detail="No data provided to update")
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    except PyMongoError:
        raise HTTPException(status_code=500, detail="Database error")

@main.delete("/data_sante/{id}")
async def delete_data(id: str):
    try:
        result = collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return {"detail": "Data deleted successfully"}
        raise HTTPException(status_code=404, detail="Data not found")
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    except PyMongoError:
        raise HTTPException(status_code=500, detail="Database error")
