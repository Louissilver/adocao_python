from bson import ObjectId
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from models.solicitacao_adocao import Solicitacao_Adocao
from config.db import conn
from schemas.solicitacao_adocao import solicitacoes_adocaoEntity, solicitacao_adocaoEntity

solicitacao_adocao = APIRouter()


@solicitacao_adocao.get('/adocao/solicitacoes')
async def find_all_solicitacoes_adocao():
    return solicitacoes_adocaoEntity(conn.local.solicitacao_adocao.find())


@solicitacao_adocao.get('/adocao/solicitacao/{id}')
async def find_one_solicitacao_adocao(id):
    return solicitacao_adocaoEntity(conn.local.solicitacao_adocao.find_one({"_id": ObjectId(id)}))


@solicitacao_adocao.post("/adocao/solicitacao")
async def create_solicitacao_adocao(solicitacao_adocao: Solicitacao_Adocao):
    _id = conn.local.solicitacao_adocao.insert_one(
        dict(solicitacao_adocao))
    id_solicitacao = _id.inserted_id
    return f"Solicitação de adoção {id_solicitacao} cadastrada com sucesso!"


@solicitacao_adocao.put('/adocao/solicitacao/{id}')
async def update_solicitacao_adocao(id, solicitacao_adocao: Solicitacao_Adocao):
    conn.local.solicitacao_adocao.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(solicitacao_adocao)
    })
    return solicitacao_adocaoEntity(conn.local.solicitacao_adocao.find_one({"_id": ObjectId(id)}))


@solicitacao_adocao.put('/adocao/solicitacao/aprovar/{id}')
async def aprovar_solicitacao_adocao(id):
    conn.local.solicitacao_adocao.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": {
            "aprovado": True
        }
    })
    return solicitacao_adocaoEntity(conn.local.solicitacao_adocao.find_one({"_id": ObjectId(id)}))


@solicitacao_adocao.put('/adocao/solicitacao/finalizar/{id}')
async def finalizar_solicitacao_adocao(id):
    conn.local.solicitacao_adocao.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": {
            "finalizado": True
        }
    })
    return solicitacao_adocaoEntity(conn.local.solicitacao_adocao.find_one({"_id": ObjectId(id)}))


@solicitacao_adocao.delete('/adocao/solicitacao/{id}')
async def delete_solicitacao_adocao(id):
    return solicitacao_adocaoEntity(conn.local.solicitacao_adocao.find_one_and_delete({"_id": ObjectId(id)}))
