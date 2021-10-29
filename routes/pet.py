from bson import ObjectId
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from models.pet import Pet
from config.db import conn
from schemas.pet import petEntity, petsEntity

pet = APIRouter()


@pet.get('/pets')
async def find_all_pets():
    return Pet.retornar_todos_pets()


@pet.get('/pets/{id}')
async def find_all_pets(id):
    return Pet.retornar_um_pet(id)


@pet.post("/pets")
async def create_pet(pet: Pet):
    pet.inserir_um_pet()
    return f"O pet {pet.nome} foi cadastrado com sucesso!"


@pet.put('/pets/{id}')
async def update_pet(id, pet: Pet):
    pet.atualizar_um_pet(id)
    return f"O pet {pet.nome} foi atualizado com sucesso!"


@pet.delete('/pets/{id}')
async def delete_pet(id):
    pet_deletado = Pet.retornar_nome_pet(id)
    Pet.deletar_um_pet(id)
    return f"O pet {pet_deletado} foi excluído com sucesso!"
