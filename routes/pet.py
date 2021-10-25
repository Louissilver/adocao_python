from bson import ObjectId
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from models.pet import Pet
from config.db import conn
from schemas.pet import petEntity, petsEntity

pet = APIRouter()


@pet.get('/pets')
async def find_all_pets():
    return petsEntity(conn.local.pet.find())


@pet.get('/pets/{id}')
async def find_all_pets(id):
    return petEntity(conn.local.pet.find_one({"_id": ObjectId(id)}))


@pet.post("/pets")
async def create_pet(pet: Pet):
    conn.local.pet.insert_one(jsonable_encoder(pet))
    return f"Pet {pet.nome} cadastrado com sucesso!"


@pet.put('/{id}')
async def update_pet(id, pet: Pet):
    conn.local.pet.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(pet)
    })
    return petEntity(conn.local.pet.find_one({"_id": ObjectId(id)}))


@pet.delete('/{id}')
async def delete_pet(id):
    return petEntity(conn.local.pet.find_one_and_delete({"_id": ObjectId(id)}))
