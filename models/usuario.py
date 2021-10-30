from typing import Optional
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from config.db import conn
from schemas.usuario import usuarioEntity, usuariosEntity


class Usuario(BaseModel):
    login: str
    senha: str
    tipo_usuario: str
    id_pessoa: Optional[str]

    @staticmethod
    def retornar_usuarios():
        return usuariosEntity(conn.local.usuario.find())

    @staticmethod
    def retornar_um_usuario(id):
        return usuarioEntity(conn.local.usuario.find_one({"_id": ObjectId(id)}))

    def inserir_usuario(self):
        return conn.local.usuario.insert_one(jsonable_encoder(self))

    def inserir_id_pessoa(self, id_usuario, id_pessoa):
        conn.local.usuario.find_one_and_update({"_id": ObjectId(id_usuario)}, {
            "$set": {
                "id_pessoa": id_pessoa
            }})

    def atualizar_usuario(self, id):
        conn.local.usuario.find_one_and_update({"_id": ObjectId(id)}, {
            "$set": dict(self)
        })

    @staticmethod
    def deletar_usuario(id_pessoa):
        conn.local.usuario.find_one_and_delete({"id_pessoa": id_pessoa})

    class Config:
        schema_extra = {
            "example": {
                "login": "ondaanimal@gmail.com",
                "senha": "12345",
                "tipo_usuario": "ONG",
            }
        }
