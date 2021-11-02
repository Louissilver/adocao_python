from os import replace
import re
from typing import Optional
from bson import ObjectId
from fastapi import HTTPException, status
from pydantic import BaseModel
from datetime import date, datetime

from pydantic.class_validators import validator
from config.db import conn
from schemas.pet import petEntity, petsEntity


class Pet(BaseModel):
    nome: str
    especie: str
    raca: str
    dataNascimento: str
    sexo: str
    porte: str
    adotado: bool
    urlFoto: str
    observacoes: str
    id_ong: str
    id_associado: Optional[str]

    @validator('nome')
    def validar_nome(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo nome é obrigatório.")
        if len(valor) <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O nome deve conter, pelo menos, 2 caracteres.")
        return valor

    @validator('especie')
    def validar_especie(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo espécie é obrigatório.")
        if len(valor) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="A espécie deve conter, pelo menos, 3 caracteres.")
        return valor
        
    @validator('raca')
    def validar_raca(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo raça é obrigatório.")
        if len(valor) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="A raça deve conter, pelo menos, 3 caracteres.")
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
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo data de nascimento é obrigatório.")
        padrao = "^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$"
        validacao = re.match(padrao, valor)
        if not validacao:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="A data informada não é válida. Tente o formado 'dd/mm/aaaa'")
        if datetime(ano, mes, dia) > datetime.now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="A data informada deve ser menor do que a data atual.")
        return valor

    @validator('sexo')
    def validar_sexo(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo sexo é obrigatório.")
        if len(valor) != 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O sexo deve conter apenas um caracter, M - Masculino, F - Feminino.")
        return valor

    @validator('porte')
    def validar_porte(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo porte é obrigatório.")
        if valor != 'Pequeno' and valor != 'Médio' and valor != 'Grande':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O porte informado é inválido. Tente 'Pequeno', 'Médio' ou 'Grande'")
        return valor

    @validator('urlFoto')
    def validar_urlFoto(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo url de imagem é obrigatório.")
        padrao = "^[a-zA-Z0-9-_]+[:./\\\]+([a-zA-Z0-9 -_./:=&\"'?%+@#$!])+$"
        validacao = re.match(padrao, valor)
        if not validacao:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="A URL informada não é válida. Tente um exemplo como 'https://www.google.com.br/'")
        return valor

    @staticmethod
    def retornar_todos_pets():
        return petsEntity(conn.adocao.pet.find())

    @staticmethod
    def ser_adotado(solicitacao):
        conn.adocao.pet.find_one_and_update({"_id": ObjectId(solicitacao["id_pet"])}, {
            "$set": {"adotado": True,
                     "id_associado": solicitacao["id_associado"]}})

    @staticmethod
    def retornar_um_pet(id):
        return petEntity(conn.adocao.pet.find_one({"_id": ObjectId(id)}))

    def inserir_um_pet(self):
        data = self.dataNascimento.split('/')
        dia, ano = int(data[0]), int(data[2])
        if(data[1][0] != 0):
            mes = int(data[1])
        else:
            mes = int(data[1].replace("0", ""))
        conn.adocao.pet.insert_one({
            "nome": self.nome,
            "especie": self.especie,
            "raca": self.raca,
            "dataNascimento": datetime(ano, mes, dia),
            "sexo": self.sexo,
            "porte": self.porte,
            "adotado": False,
            "urlFoto": self.urlFoto,
            "observacoes": self.observacoes,
            "id_ong": self.id_ong
        })

    def atualizar_um_pet(self, id):
        data = self.dataNascimento.split('/')
        dia, ano = int(data[0]), int(data[2])
        if(data[1][0] != 0):
            mes = int(data[1])
        else:
            mes = int(data[1].replace("0", ""))
        conn.adocao.pet.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": {
                "nome": self.nome,
                "especie": self.especie,
                "raca": self.raca,
                "dataNascimento": datetime(ano, mes, dia),
                "sexo": self.sexo,
                "porte": self.porte,
                "adotado": False,
                "urlFoto": self.urlFoto,
                "observacoes": self.observacoes,
                "id_ong": self.id_ong
            }})

    @staticmethod
    def retornar_nome_pet(id):
        return petEntity(conn.adocao.pet.find_one({"_id": ObjectId(id)}))["nome"]

    @staticmethod
    def deletar_um_pet(id):
        conn.adocao.pet.find_one_and_delete({"_id": ObjectId(id)})

    class Config:
        schema_extra = {
            "example": {
                "nome": "Rubídio",
                "especie": "Cachorro",
                "raca": "SRD",
                "dataNascimento": "14/02/2018",
                "sexo": "M",
                "porte": "Médio",
                "adotado": False,
                "urlFoto": "https://4.bp.blogspot.com/_gWqerMk_ui0/Rvq7ZbayoEI/AAAAAAAAA8Q/xU696jlpw68/s320/Rabbit.jpg",
                "observacoes": "Cãozinho muito dócil, brincalhão, companheiro. Adora dormir com a cabeça no travesseiro",
                "id_ong": "617e8e858256696f8259915d"
            }
        }
