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
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo telefone é obrigatório.")
        padrao = "^\(?\d{2}\)?[\s-]?[\s9]?\d{4}-?\d{4}$"
        validacao = re.match(padrao, valor)
        if not validacao:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O telefone informado não é válido. Tente o formato '(XX)XXXXX-XXXX'")
        return valor

    def inserir_pessoa(self):
        return conn.adocao.pessoa.insert_one({
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "endereco": jsonable_encoder(self.endereco)
        })

    @staticmethod
    def retornar_uma_pessoa(id):
        return pessoaEntity(conn.adocao.pessoa.find_one({"_id": ObjectId(id)}))

    @staticmethod
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
    def deletar_pessoa(id_pessoa):
        conn.adocao.pessoa.find_one_and_delete({"_id": ObjectId(id_pessoa)})

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
