from datetime import datetime, timedelta
import re
from typing import Optional
from bson import ObjectId
from fastapi import HTTPException, status
from jose.constants import ALGORITHMS
from pydantic import BaseModel
from pydantic import validator
from config.db import conn
from schemas.usuario import usuarioEntity, usuariosEntity
from passlib.context import CryptContext
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


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
    def autenticar_usuario(login, senha):
        usuario = Usuario.retornar_login_e_senha(login)

        if usuario:
            password_check = pwd_context.verify(senha, usuario["senha"])
            return password_check
        else:
            return False

    @staticmethod
    def criar_token_de_acesso(data: dict, expires_delta: timedelta):
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})

        load_dotenv()
        SECRET_KEY = os.getenv('SECRET_KEY')
        ALGORITHM = os.getenv('ALGORITHM')

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt

    @staticmethod
    def get_passwordhash(password):
        return pwd_context.hash(password)

    @staticmethod
    def retornar_usuarios():
        return usuariosEntity(conn.adocao.usuario.find())

    @staticmethod
    def retornar_logins_existentes(id=None):
        logins = []
        for usuario in usuariosEntity(conn.adocao.usuario.find()):
            logins.append(usuario["login"])
        if id != None:
            logins.remove(Usuario.retornar_um_usuario(id)["login"])
        return logins

    @staticmethod
    def retornar_um_usuario(id):
        return usuarioEntity(conn.adocao.usuario.find_one({"_id": ObjectId(id)}))

    @staticmethod
    def retornar_login_e_senha(login):
        if conn.adocao.usuario.find({"login": login}).count() > 0:
            return usuarioEntity(conn.adocao.usuario.find_one({"login": login}))
        return []

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
