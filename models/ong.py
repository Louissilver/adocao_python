import re
from typing import Optional
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status
from pydantic import validator
from models.pessoa import Pessoa
from schemas.ong import ongEntity, ongsEntity
from config.db import conn


class Ong(Pessoa):
    cnpj: str
    id_pessoa: Optional[str]

    @validator('cnpj')
    def validar_cpf(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo CNPJ é obrigatório.")
        padrao = "^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$"
        validacao = re.match(padrao, valor)
        if not validacao:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O CNPJ informado não é válido. Tente o formato XX.XXX.XXX/XXXX-XX")
        return valor

    @staticmethod
    def retornar_ongs():
        return ongsEntity(conn.local.ong.find())

    @staticmethod
    def retornar_uma_ong(id):
        return ongEntity(conn.local.ong.find_one({"_id": ObjectId(id)}))

    def inserir_ong(self):
        return conn.local.ong.insert_one({
            "cnpj": self.cnpj,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "endereco": jsonable_encoder(self.endereco)
        })

    def inserir_id_pessoa(self, id_ong, id_pessoa):
        return conn.local.ong.find_one_and_update({"_id": ObjectId(id_ong)}, {
            "$set": {
                "id_pessoa": id_pessoa
            }})

    def atualizar_ong(self, id):
        conn.local.ong.find_one_and_update({"_id": ObjectId(id)}, {
            "$set": {
                "cnpj": self.cnpj,
                "nome": self.nome,
                "email": self.email,
                "telefone": self.telefone,
                "endereco": jsonable_encoder(self.endereco)
            }
        })

    @staticmethod
    def retornar_nome_ong(id):
        return ongEntity(conn.local.ong.find_one(
            {"_id": ObjectId(id)}))["nome"]

    @staticmethod
    def retornar_id_pessoa(id):
        return ongEntity(conn.local.ong.find_one(
            {"_id": ObjectId(id)}))["id_pessoa"]

    @staticmethod
    def deletar_ong(id):
        conn.local.ong.find_one_and_delete({"_id": ObjectId(id)})

    class Config:
        schema_extra = {
            "example": {
                "cnpj": "65.705.048/0001-40",
                "nome": "Projeto Lontra",
                "email": "plontra@gmail.com.br",
                "telefone": "(51)94948-7887",
                "endereco": {
                    "cep": "93244-850",
                    "logradouro": "Av. das Missões",
                    "numero": 222,
                    "bairro": "Canoas",
                    "cidade": "Porto Alegre",
                    "estado": "RS"
                }
            }
        }
