from fastapi import APIRouter
from models.pet import Pet
from fastapi import status

pet = APIRouter()


@pet.get('/pets', status_code=status.HTTP_200_OK)
async def find_all_pets():
    return Pet.retornar_todos_pets()


@pet.get('/pets/{id}', status_code=status.HTTP_200_OK)
async def find_all_pets(id):
    return Pet.retornar_um_pet(id)


@pet.post("/pets", status_code=status.HTTP_200_OK)
async def create_pet(pet: Pet):
    pet.inserir_um_pet()
    return f"O pet {pet.nome} foi cadastrado com sucesso!"


@pet.put('/pets/{id}', status_code=status.HTTP_200_OK)
async def update_pet(id, pet: Pet):
    pet.atualizar_um_pet(id)
    return f"O pet {pet.nome} foi atualizado com sucesso!"


@pet.delete('/pets/{id}', status_code=status.HTTP_200_OK)
async def delete_pet(id):
    pet_deletado = Pet.retornar_nome_pet(id)
    Pet.deletar_um_pet(id)
    return f"O pet {pet_deletado} foi excluído com sucesso!"
