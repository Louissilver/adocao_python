from typing import List, Optional
from datetime import datetime

from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from schemas.associado import associadoEntity, associadosEntity
from config.db import conn
from models.pessoa import Pessoa


class Associado(Pessoa):
    cpf: str
    dataNascimento: datetime
    animaisAdotados: Optional[List[str]]
    id_pessoa: Optional[str]

    @staticmethod
    def retornar_associados():
        return associadosEntity(conn.local.associado.find())

    @staticmethod
    def retornar_uma_associado(id):
        return associadoEntity(conn.local.associado.find_one({"_id": ObjectId(id)}))

    def inserir_associado(self):
        return conn.local.associado.insert_one(jsonable_encoder(self))

    def inserir_id_pessoa(self, id_associado, id_pessoa):
        return conn.local.associado.find_one_and_update({"_id": ObjectId(id_associado)}, {
            "$set": {
                "id_pessoa": id_pessoa
            }})

    def atualizar_associado(self, id):
        conn.local.associado.find_one_and_update({"_id": ObjectId(id)}, {
            "$set": {
                "cpf": self.cpf,
                "nome": self.nome,
                "email": self.email,
                "telefone": self.telefone,
                "endereco": jsonable_encoder(self.endereco),
                "dataNascimento": self.dataNascimento,
                "animaisAdotados": self.animaisAdotados
            }
        })

    @staticmethod
    def retornar_nome_associado(id):
        return associadoEntity(conn.local.associado.find_one({"_id": ObjectId(id)}))["nome"]

    @staticmethod
    def deletar_associado(id):
        conn.local.associado.find_one_and_delete(
            {"_id": ObjectId(id)})

    @staticmethod
    def retornar_id_pessoa(id):
        return associadoEntity(conn.local.associado.find_one(
            {"_id": ObjectId(id)}))["id_pessoa"]

    class Config:
        schema_extra = {
            "example": {
                "nome": "Luís Fernando da Silveira",
                "email": "luis.202020718@unilasalle.edu.br",
                "telefone": "51995814416",
                "endereco": {
                    "cep": "93600000",
                    "logradouro": "Av. das Rosas",
                    "numero": 1410,
                    "bairro": "Floresta",
                    "cidade": "Estância Velha",
                    "estado": "RS"
                },
                "cpf": "45396497289",
                "dataNascimento": datetime(1999, 3, 19),
                "animaisAdotados": [],
            }
        }
