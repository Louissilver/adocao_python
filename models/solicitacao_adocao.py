from bson import ObjectId
from pydantic import BaseModel
from datetime import datetime
from config.db import conn
from schemas.solicitacao_adocao import solicitacao_adocaoEntity, solicitacoes_adocaoEntity


class Solicitacao_Adocao(BaseModel):
    id_associado: str
    id_ong: str
    id_pet: str
    aprovado: bool
    finalizado: bool
    referencias: str
    dataSolicitacao: datetime

    @staticmethod
    def retornar_solicitacoes():
        return solicitacoes_adocaoEntity(conn.local.solicitacao_adocao.find())

    @staticmethod
    def retornar_uma_solicitacao(id):
        return solicitacao_adocaoEntity(conn.local.solicitacao_adocao.find_one({"_id": ObjectId(id)}))

    def inserir_solicitacao(self):
        return conn.local.solicitacao_adocao.insert_one(dict(self))

    def atualizar_solicitacao(self, id):
        conn.local.solicitacao_adocao.find_one_and_update({"_id": ObjectId(id)}, {
            "$set": dict(self)
        })

    @staticmethod
    def aprovar_solicitacao(id):
        conn.local.solicitacao_adocao.find_one_and_update({"_id": ObjectId(id)}, {
            "$set": {
                "aprovado": True
            }
        })
        return Solicitacao_Adocao.retornar_id_solicitacao(id)

    @staticmethod
    def finalizar_solicitacao(id):
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
                "aprovado": False,
                "finalizado": False,
                "referencias": "Tenho um filho que ama animais, um pátio enorme e atualmente já cuido ...",
                "dataSolicitacao": datetime.now(),
            }
        }
