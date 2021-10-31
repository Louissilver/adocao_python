from typing import Optional
from bson import ObjectId
from fastapi import HTTPException, status
from pydantic import BaseModel
from datetime import datetime
from pydantic import validator
from config.db import conn
from models.associado import Associado
from models.pet import Pet
from schemas.solicitacao_adocao import solicitacao_adocaoEntity, solicitacoes_adocaoEntity


class Solicitacao_Adocao(BaseModel):
    id_associado: str
    id_ong: str
    id_pet: str
    aprovado: Optional[bool]
    finalizado: Optional[bool]
    referencias: str
    dataSolicitacao: Optional[datetime]

    @validator('id_associado')
    def validar_id_associado(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo id_associado é obrigatório.")
        return valor

    @validator('id_ong')
    def validar_id_ong(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo id_ong é obrigatório.")
        return valor

    @validator('id_pet')
    def validar_id_pet(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo id_pet é obrigatório.")
        return valor

    @validator('referencias')
    def validar_referencias(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo referencias é obrigatório.")
        if len(valor) < 30 or (' ' not in valor):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="As referências informadas devem conter, pelo menos, 30 caracteres e espaços, formando um texto.")
        return valor

    @staticmethod
    def retornar_solicitacoes():
        return solicitacoes_adocaoEntity(conn.local.solicitacao_adocao.find())

    @staticmethod
    def retornar_uma_solicitacao(id):
        return solicitacao_adocaoEntity(conn.local.solicitacao_adocao.find_one({"_id": ObjectId(id)}))

    def inserir_solicitacao(self):
        return conn.local.solicitacao_adocao.insert_one({
            "id_associado": self.id_associado,
            "id_ong": self.id_ong,
            "id_pet": self.id_pet,
            "aprovado": False,
            "finalizado": False,
            "referencias": self.referencias,
            "dataSolicitacao": datetime.now(),
        })

    def atualizar_solicitacao(self, id):
        conn.local.solicitacao_adocao.find_one_and_update({"_id": ObjectId(id)}, {
            "$set": {
                "id_associado": self.id_associado,
                "id_ong": self.id_ong,
                "id_pet": self.id_pet,
                "referencias": self.referencias,
            }
        })

    @staticmethod
    def aprovar_solicitacao(id):
        solicitacao = Solicitacao_Adocao.retornar_uma_solicitacao(id)
        if solicitacao["aprovado"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="A solicitação já foi aprovada")
        conn.local.solicitacao_adocao.find_one_and_update({"_id": ObjectId(id)}, {
            "$set": {
                "aprovado": True
            }
        })
        return Solicitacao_Adocao.retornar_id_solicitacao(id)

    @staticmethod
    def finalizar_solicitacao(id):
        solicitacao = Solicitacao_Adocao.retornar_uma_solicitacao(id)
        if solicitacao["finalizado"] == True:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="A solicitação já foi finalizada")
        if solicitacao["aprovado"]:
            Associado.incluir_pet(solicitacao)
            Pet.ser_adotado(solicitacao)
        conn.local.solicitacao_adocao.find_one_and_update({"_id": ObjectId(id)}, {
            "$set": {
                "finalizado": True
            }
        })
        return Solicitacao_Adocao.retornar_id_solicitacao(id)

    @staticmethod
    def retornar_id_solicitacao(id):
        return solicitacao_adocaoEntity(conn.local.solicitacao_adocao.find_one({"_id": ObjectId(id)}))["id"]

    @staticmethod
    def deletar_solicitacao(id):
        conn.local.solicitacao_adocao.find_one_and_delete(
            {"_id": ObjectId(id)})

    class Config:
        schema_extra = {
            "example": {
                "id_associado": "6171db8444806f2e8000bf42",
                "id_ong": "6171db6244806f2e8000bf41",
                "id_pet": "6171dbb644806f2e8000bf45",
                "referencias": "Tenho um filho que ama animais, um pátio enorme e atualmente já cuido ...",
            }
        }
