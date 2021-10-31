import re
from typing import List, Optional
from datetime import date, datetime
from pydantic import validator
from bson import ObjectId
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from schemas.associado import associadoEntity, associadosEntity
from config.db import conn
from models.pessoa import Pessoa


class Associado(Pessoa):
    cpf: str
    dataNascimento: str
    animaisAdotados: Optional[List[str]]
    id_pessoa: Optional[str]

    @validator('cpf')
    def validar_cpf(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo CPF é obrigatório.")
        padrao = "^\d{3}\.\d{3}\.\d{3}\-\d{2}$"
        validacao = re.match(padrao, valor)
        if not validacao:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O CPF informado não é válido. Tente o formato 'XXX.XXX.XXX-XX'")
        return valor

    @validator('dataNascimento')
    def validar_dataNascimento(cls, valor):
        valor = valor.strip()
        data = valor.split('/')
        dia, ano = int(data[0]), int(data[2])
        if(data[1][0] != 0):
            mes = int(data[1])
        else:
            mes = int(data[1].replace("0", ""))
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo dataNascimento é obrigatório.")
        padrao = "^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$"
        validacao = re.match(padrao, valor)
        if not validacao:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="A data informada não é válida.")
        if datetime(ano, mes, dia) > datetime.now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="A data informada deve ser menor do que a data atual.")
        return valor

    @staticmethod
    def retornar_associados():
        return associadosEntity(conn.local.associado.find())

    @staticmethod
    def retornar_um_associado(id):
        ids = []
        for i in Associado.retornar_associados():
            ids.append(i["id"])
        if id not in ids:
            raise HTTPException(
                status_code=404, detail="Não foi possível encontrar nenhum associado com esse id.")
        return associadoEntity(conn.local.associado.find_one({"_id": ObjectId(id)}))

    def inserir_associado(self):
        data = self.dataNascimento.split('/')
        dia, ano = int(data[0]), int(data[2])
        if(data[1][0] != 0):
            mes = int(data[1])
        else:
            mes = int(data[1].replace("0", ""))
        return conn.local.associado.insert_one({
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "endereco": jsonable_encoder(self.endereco),
            "cpf": self.cpf,
            "dataNascimento": datetime(ano, mes, dia),
            "animaisAdotados": self.animaisAdotados,
        })

    def inserir_id_pessoa(self, id_associado, id_pessoa):
        return conn.local.associado.find_one_and_update({"_id": ObjectId(id_associado)}, {
            "$set": {
                "id_pessoa": id_pessoa
            }})

    def atualizar_associado(self, id):
        data = self.dataNascimento.split('/')
        dia, ano = int(data[0]), int(data[2])
        if(data[1][0] != 0):
            mes = int(data[1])
        else:
            mes = int(data[1].replace("0", ""))
        conn.local.associado.find_one_and_update({"_id": ObjectId(id)}, {
            "$set": {
                "nome": self.nome,
                "email": self.email,
                "telefone": self.telefone,
                "endereco": jsonable_encoder(self.endereco),
                "cpf": self.cpf,
                "dataNascimento": datetime(ano, mes, dia),
                "animaisAdotados": self.animaisAdotados,
            }
        })

    @staticmethod
    def retornar_nome_associado(id):
        return associadoEntity(conn.local.associado.find_one({"_id": ObjectId(id)}))["nome"]

    @staticmethod
    def incluir_pet(solicitacao):
        conn.local.associado.find_one_and_update({"_id": ObjectId(solicitacao["id_associado"])}, {
            "$push": {"animaisAdotados": solicitacao["id_pet"]}})

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
                "telefone": "(51)99581-4416",
                "endereco": {
                    "cep": "93600-000",
                    "logradouro": "Av. das Rosas",
                    "numero": 1410,
                    "bairro": "Floresta",
                    "cidade": "Estância Velha",
                    "estado": "RS"
                },
                "cpf": "453.964.972-89",
                "dataNascimento": "19/03/2019",
                "animaisAdotados": [],
            }
        }
