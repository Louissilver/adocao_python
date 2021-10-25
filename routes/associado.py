from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from fastapi.routing import APIRoute, APIRouter
from config.db import conn
from models.pessoa import Pessoa
from models.associado import Associado
from models.usuario import Usuario
from schemas.associado import associadoEntity, associadosEntity

associado = APIRouter()


@associado.get('/associados')
async def find_all_associados():
    return associadosEntity(conn.local.associado.find())


@associado.get('/associados/{id}')
async def find_one_associado(id):
    return associadoEntity(conn.local.associado.find_one({"_id": ObjectId(id)}))


@associado.post("/associados")
async def create_associado(associado: Associado, usuario: Usuario):
    _id_pessoa = conn.local.pessoa.insert_one({
        "nome": associado.nome,
        "email": associado.email,
        "telefone": associado.telefone,
        "endereco": jsonable_encoder(associado.endereco)
    })
    id_pessoa = str(_id_pessoa.inserted_id)
    _id_associado = conn.local.associado.insert_one(
        jsonable_encoder(associado))
    id_associado = str(_id_associado.inserted_id)
    conn.local.associado.find_one_and_update({"_id": ObjectId(id_associado)}, {
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
    return f"Pessoa {associado.nome} inserida com sucesso!"


@associado.put('/associados/{id}')
async def update_associado(id, associado: Associado):
    conn.local.associado.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(associado)
    })
    return associadoEntity(conn.local.associado.find_one({"_id": ObjectId(id)}))


@associado.delete('/associados/{id}')
async def delete_associado(id):
    pessoa = dict(conn.local.associado.find_one({"_id": ObjectId(id)}))
    id_pessoa = str(pessoa["id_pessoa"])
    conn.local.usuario.find_one_and_delete({"id_pessoa": id_pessoa})
    conn.local.pessoa.find_one_and_delete({"_id": ObjectId(id_pessoa)})
    conn.local.associado.find_one_and_delete({"_id": ObjectId(id)})
    return f"Pessoa {id_pessoa}"
