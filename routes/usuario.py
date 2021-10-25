from bson import ObjectId
from fastapi.routing import APIRouter
from config.db import conn
from models.usuario import Usuario
from schemas.usuario import usuarioEntity, usuariosEntity

usuario = APIRouter()


@usuario.get('/usuarios')
async def find_all_usuarios():
    return usuariosEntity(conn.local.usuario.find())


@usuario.get('/usuarios/{id}')
async def find_one_usuario(id):
    return usuarioEntity(conn.local.usuario.find_one({"_id": ObjectId(id)}))


@usuario.put('/usuarios/{id}')
async def update_usuario(id, usuario: Usuario):
    conn.local.usuario.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(usuario)
    })
    return usuarioEntity(conn.local.usuario.find_one({"_id": ObjectId(id)}))
