from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, validator
from config.db import conn
from models.endereco import Endereco
from email_validator import EmailNotValidError, validate_email
import re
from fastapi import status
from schemas.pessoa import pessoaEntity, pessoasEntity


class Pessoa(BaseModel):
    nome: str
    email: str
    telefone: str
    endereco: Endereco

# Validadores
    @validator('nome')
    def validar_nome(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo nome é obrigatório.")
        if len(valor) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O nome deve conter, pelo menos, 3 caracteres.")
        return valor

    @validator('email', pre=True)
    def validar_email(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo e-mail é obrigatório.")
        try:
            valid = validate_email(valor)
            valor = valid.email
        except EmailNotValidError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O e-mail informado não é válido. Tente o formato 'email@example.com'")
        return valor

    @validator('telefone', pre=True)
    def validar_telefone(cls, valor):
        valor = valor.strip()
        padrao = "^\(?\d{2}\)?[\s-]?[\s9]?\d{4}-?\d{4}$"
        validacao = re.match(padrao, valor)
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo telefone é obrigatório.")
        if not validacao:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O telefone informado não é válido. Tente o formato '(XX)XXXXX-XXXX'")
        return valor

# Métodos de instância

    # Objetivo: Inserir no banco um registro de pessoa utilizando os atributos da classe
    # Parâmetros:
    # Retorno: Objeto MongoClient
    def inserir_pessoa(self):
        return conn.adocao.pessoa.insert_one({
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "endereco": jsonable_encoder(self.endereco)
        })

# Métodos estáticos

    @staticmethod
    # Objetivo: Encontrar a pessoa que possua o id passado por parâmetro e retornar um dicionário com keys/values da pessoa encontrada
    # Parâmetros: id: str
    # Retorno: Dicionário contendo keys/values da pessoa cadastrada
    def retornar_uma_pessoa(id):
        return pessoaEntity(conn.adocao.pessoa.find_one({"_id": ObjectId(id)}))

    @staticmethod
    # Objetivo: Retornar uma lista contendo todos os e-mails cadastrados
    # Parâmetros: id: str
    # Retorno: Lista de str contendo e-mails
    def retornar_emails_existentes(id=None):
        emails = []
        if conn.adocao.pessoa.find().count() > 0:
            pessoas = pessoasEntity(conn.adocao.pessoa.find())
            for pessoa in pessoas:
                emails.append(pessoa["email"])
            if id != None:
                emails.remove(
                    Pessoa.retornar_uma_pessoa(id)["email"])
        return emails

    @staticmethod
    # Objetivo: Encontrar uma pessoa através do id e deletar o cadastro
    # Parâmetros: id_pessoa: str
    # Retorno:
    def deletar_pessoa(id_pessoa):
        conn.adocao.pessoa.find_one_and_delete({"_id": ObjectId(id_pessoa)})

# Exemplo de esquema
    class Config:
        schema_extra = {
            "example": {
                "nome": "Luís Fernando da Silveira",
                "email": "luis.202020718@unilasalle.edu.br",
                "telefone": "(51)99581-4416",
                "endereco": {
                    "cep": "93600-000",
                    "logradouro": "Av. das Rosas",
                    "numero": 1410,
                    "bairro": "Floresta",
                    "cidade": "Estância Velha",
                    "estado": "RS"
                }
            }
        }
