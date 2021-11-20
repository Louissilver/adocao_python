from datetime import datetime, timedelta
import re
from typing import Optional
from bson import ObjectId
from fastapi import HTTPException, status
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

# Validadores

    @validator('login')
    def validar_login(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo login é obrigatório.")
        if len(valor) < 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O login deve conter, pelo menos, 5 caracteres.")
        return valor

    @validator('senha')
    def validar_senha(cls, valor):
        valor = valor.strip()
        padrao = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        validacao = re.match(padrao, valor)
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo senha é obrigatório.")
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

# Métodos de instância

    # Objetivo: Inserir no banco um registro de usuário utilizando os atributos da classe
    # Parâmetros:
    # Retorno: Objeto MongoClient
    def inserir_usuario(self):
        return conn.adocao.usuario.insert_one({
            "login": self.login,
            "senha": self.senha,
            "tipo_usuario": self.tipo_usuario
        })

    # Objetivo: Encontrar um usuário através do id e atualizar os campos com os atributos da classe
    # Parâmetros: id: str
    # Retorno:
    def atualizar_usuario(self, id):
        conn.adocao.usuario.find_one_and_update({"_id": ObjectId(id)}, {
            "$set": {
                "login": self.login,
                "senha": self.senha,
            }
        })

    # Objetivo: Encontrar um usuário através do id_usuario e incluir o id_pessoa
    # Parâmetros: id_usuario: str, id_pessoa: str
    # Retorno:
    def inserir_id_pessoa(self, id_usuario, id_pessoa):
        conn.adocao.usuario.find_one_and_update({"_id": ObjectId(id_usuario)}, {
            "$set": {
                "id_pessoa": id_pessoa
            }})

# Métodos estáticos

    @staticmethod
    # Objetivo: Retornar o nome de usuário logado na aplicação
    # Parâmetros: token: str
    # Retorno: str com nome do usuário logado
    def retornar_usuario_atual(token):
        load_dotenv()
        SECRET_KEY = os.getenv('SECRET_KEY')
        ALGORITHM = os.getenv('ALGORITHM')
        try:
            decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            usuario = decoded_jwt.get('sub')
        except:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha incorretos.")
        return usuario

    @staticmethod
    # Objetivo: Retornar o tipo de usuário logado na aplicação
    # Parâmetros: usuario_atual: str
    # Retorno: str com tipo do usuário logado
    def retornar_tipo_usuario(usuario_atual):
        tipo_usuario = usuarioEntity(conn.adocao.usuario.find_one(
            {"login": usuario_atual}))["tipo_usuario"]
        id_pessoa = usuarioEntity(conn.adocao.usuario.find_one(
            {"login": usuario_atual}))["id_pessoa"]
        id_usuario = str(usuarioEntity(conn.adocao.usuario.find_one(
            {"login": usuario_atual}))["id"])
        return [tipo_usuario, id_pessoa, id_usuario]

    @staticmethod
    # Objetivo: Realizar a autenticação do login e senha informados e retornar se está de acordo
    # Parâmetros: login: str, senha: str
    # Retorno: bool para autenticação realizada
    def autenticar_usuario(login, senha):
        usuario = Usuario.retornar_login_e_senha(login)
        if usuario:
            password_check = pwd_context.verify(senha, usuario["senha"])
            return password_check
        else:
            return False

    @staticmethod
    # Objetivo: Retornar um token de acesso gerado
    # Parâmetros: data: dict, expires_delta: timedelta
    # Retorno: str com token jwt gerado
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
    # Objetivo: Retornar a senha em forma de hash criptografada
    # Parâmetros: password: str
    # Retorno: str hash de senha gerada
    def get_passwordhash(password):
        return pwd_context.hash(password)

    @staticmethod
    # Objetivo: Retornar uma lista com todos os usuários cadastrados
    # Parâmetros:
    # Retorno: Lista de dicionários contendo os usuários cadastrados
    def retornar_usuarios():
        return usuariosEntity(conn.adocao.usuario.find())

    @staticmethod
    # Objetivo: Retornar uma lista contendo todos os logins cadastrados
    # Parâmetros: id: str
    # Retorno: Lista de str contendo logins
    def retornar_logins_existentes(id=None):
        logins = []
        for usuario in usuariosEntity(conn.adocao.usuario.find()):
            logins.append(usuario["login"])
        if id != None:
            logins.remove(Usuario.retornar_um_usuario(id)["login"])
        return logins

    @staticmethod
    # Objetivo: Encontrar o usuário que possua o id passado por parâmetro e retornar um dicionário com keys/values do usuário encontrado
    # Parâmetros: id: str
    # Retorno: Dicionário contendo keys/values do usuário cadastrado
    def retornar_um_usuario(id):
        return usuarioEntity(conn.adocao.usuario.find_one({"_id": ObjectId(id)}))

    @staticmethod
    # Objetivo: Encontrar o usuário que possua o login passado por parâmetro e retornar um dicionário com keys/values do usuário encontrado
    # Parâmetros: login: str
    # Retorno: Dicionário contendo keys/values do usuário cadastrado
    def retornar_usuario_por_login(login):
        consulta = conn.adocao.usuario.find_one({"login": login})
        print(consulta['login'])
        if consulta == None:
            return
        else:
            return usuarioEntity(conn.adocao.usuario.find_one(
                {"login": login}))["login"]

    @staticmethod
    # Objetivo: Encontrar o usuário que possua o login passado por parâmetro e retornar um dicionário com keys/values do usuário encontrado
    # Parâmetros: login: str
    # Retorno: Dicionário contendo keys/values do usuário cadastrado
    def retornar_login_e_senha(login):
        if conn.adocao.usuario.find({"login": login}).count() > 0:
            return usuarioEntity(conn.adocao.usuario.find_one({"login": login}))
        return []

    @staticmethod
    # Objetivo: Encontrar um usuário através do id e deletar o cadastro
    # Parâmetros: id: str
    # Retorno:
    def deletar_usuario(id_pessoa):
        conn.adocao.usuario.find_one_and_delete({"id_pessoa": id_pessoa})

# Exemplo de esquema

    class Config:
        schema_extra = {
            "example": {
                "login": "teste@gmail.com",
                "senha": "Money1234!",
            }
        }
