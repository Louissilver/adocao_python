import re
from typing import Optional
from bson import ObjectId
from fastapi import HTTPException, status
from pydantic import BaseModel
from pydantic import validator
from config.db import conn
from schemas.usuario import usuarioEntity, usuariosEntity


class Usuario(BaseModel):
    login: str
    senha: str
    tipo_usuario: Optional[str]
    id_pessoa: Optional[str]

    @validator('login')
    def validar_login(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo login é obrigatório.")
        if len(valor) < 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O login deve conter, pelo menos, 5 caracteres")
        return valor

    @validator('senha')
    def validar_senha(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo login é obrigatório.")
        padrao = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        validacao = re.match(padrao, valor)
        if not validacao:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="A senha informada deve conter: mínimo de oito caracteres, pelo menos uma letra maiúscula, uma letra minúscula, um número e um caractere especial.")
        return valor

    @validator('tipo_usuario')
    def validar_tipo_usuario(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo tipo_usuario é obrigatório.")
        if valor != "ONG" and valor != "Associado":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O tipo de usuário é inválido. Deve ser 'ONG' ou 'Associado'")
        return valor

    @staticmethod
    def retornar_usuarios():
        return usuariosEntity(conn.adocao.usuario.find())

    @staticmethod
    def retornar_logins_existentes():
        logins = []
        for usuario in usuariosEntity(conn.adocao.usuario.find()):
            logins.append(usuario["login"])
        return logins

    @staticmethod
    def retornar_um_usuario(id):
        return usuarioEntity(conn.adocao.usuario.find_one({"_id": ObjectId(id)}))

    def inserir_usuario(self):
        return conn.adocao.usuario.insert_one({
            "login": self.login,
            "senha": self.senha,
            "tipo_usuario": self.tipo_usuario
        })

    def inserir_id_pessoa(self, id_usuario, id_pessoa):
        conn.adocao.usuario.find_one_and_update({"_id": ObjectId(id_usuario)}, {
            "$set": {
                "id_pessoa": id_pessoa
            }})

    def atualizar_usuario(self, id):
        conn.adocao.usuario.find_one_and_update({"_id": ObjectId(id)}, {
            "$set": {
                "login": self.login,
                "senha": self.senha,
                "tipo_usuario": self.tipo_usuario,
            }
        })

    @staticmethod
    def deletar_usuario(id_pessoa):
        conn.adocao.usuario.find_one_and_delete({"id_pessoa": id_pessoa})

    class Config:
        schema_extra = {
            "example": {
                "login": "teste@gmail.com",
                "senha": "Money1234!",
            }
        }
