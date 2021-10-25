from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from fastapi.routing import APIRouter
from config.db import conn
from models.pessoa import Pessoa
from models.ong import Ong
from models.usuario import Usuario
from schemas.ong import ongEntity, ongsEntity

ong = APIRouter()


@ong.get('/ongs')
async def find_all_ongs():
    return ongsEntity(conn.local.ong.find())


@ong.get('/{id}')
async def find_one_ong(id):
    return ongEntity(conn.local.ong.find_one({"_id": ObjectId(id)}))


@ong.post("/ongs")
async def create_ong(ong: Ong, usuario: Usuario):
    _id_pessoa = conn.local.pessoa.insert_one({
        "nome": ong.nome,
        "email": ong.email,
        "telefone": ong.telefone,
        "endereco": jsonable_encoder(ong.endereco)
    })
    id_pessoa = str(_id_pessoa.inserted_id)
    _id_ong = conn.local.ong.insert_one(
        jsonable_encoder(ong))
    id_ong = str(_id_ong.inserted_id)
    conn.local.ong.find_one_and_update({"_id": ObjectId(id_ong)}, {
        "$set": {
            "id_pessoa": id_pessoa
        }})
    _id_usuario = conn.local.usuario.insert_one(
        jsonable_encoder(usuario))
    id_usuario = str(_id_usuario.inserted_id)
    conn.local.usuario.find_one_and_update({"_id": ObjectId(id_usuario)}, {
        "$set": {
            "id_pessoa": id_pessoa
        }})
    return f"ONG {ong.nome} inserida com sucesso!"


@ong.put('/adocao/solicitacao/{id}')
async def update_ong(id, ong: Ong):
    conn.local.ong.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(ong)
    })
    return ongEntity(conn.local.ong.find_one({"_id": ObjectId(id)}))


@ong.delete('/adocao/solicitacao/{id}')
async def delete_ong(id):
    return ongEntity(conn.local.ong.find_one_and_delete({"_id": ObjectId(id)}))
