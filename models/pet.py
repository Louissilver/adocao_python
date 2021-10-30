from typing import Optional
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from datetime import datetime
from config.db import conn
from schemas.pet import petEntity, petsEntity


class Pet(BaseModel):
    nome: str
    especie: str
    raca: str
    dataNascimento: datetime
    sexo: str
    porte: str
    adotado: bool
    urlFoto: str
    observacoes: str
    id_ong: Optional[str]
    id_associado: Optional[str]

    @staticmethod
    def retornar_todos_pets():
        return petsEntity(conn.local.pet.find())

    @staticmethod
    def retornar_um_pet(id):
        return petEntity(conn.local.pet.find_one({"_id": ObjectId(id)}))

    def inserir_um_pet(self):
        conn.local.pet.insert_one(jsonable_encoder(self))

    def atualizar_um_pet(self, id):
        conn.local.pet.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": dict(self)})

    @staticmethod
    def retornar_nome_pet(id):
        return petEntity(conn.local.pet.find_one({"_id": ObjectId(id)}))["nome"]

    @staticmethod
    def deletar_um_pet(id):
        conn.local.pet.find_one_and_delete({"_id": ObjectId(id)})

    class Config:
        schema_extra = {
            "example": {
                "nome": "Rubídio",
                "especie": "Cachorro",
                "raca": "SRD",
                "dataNascimento": datetime(2018, 3, 26),
                "sexo": "M",
                "porte": "Médio",
                "adotado": False,
                "urlFoto": "https://4.bp.blogspot.com/_gWqerMk_ui0/Rvq7ZbayoEI/AAAAAAAAA8Q/xU696jlpw68/s320/Rabbit.jpg",
                "observacoes": "Cãozinho muito dócil, brincalhão, companheiro. Adora dormir com a cabeça no travesseiro",
            }
        }
