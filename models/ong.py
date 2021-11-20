import re
from typing import Optional
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status
from pydantic import validator
from models.pessoa import Pessoa
from schemas.ong import ongEntity, ongsEntity
from config.db import conn
from schemas.pessoa import pessoasEntity


class Ong(Pessoa):
    cnpj: str
    id_pessoa: Optional[str]

# Validadores
    @validator('cnpj')
    def validar_cpf(cls, valor):
        valor = valor.strip()
        padrao = "^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$"
        validacao = re.match(padrao, valor)
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo CNPJ é obrigatório.")
        if not validacao:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O CNPJ informado não é válido. Tente o formato 'XX.XXX.XXX/XXXX-XX'")
        return valor

# Métodos de instância

    # Objetivo: Inserir no banco um registro de ONG utilizando os atributos da classe
    # Parâmetros:
    # Retorno: Objeto MongoClient

    def inserir_ong(self):
        return conn.adocao.ong.insert_one({
            "cnpj": self.cnpj,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "endereco": jsonable_encoder(self.endereco)
        })

    # Objetivo: Encontrar uma ONG através do id_ong e incluir o id_pessoa
    # Parâmetros: id_ong: str, id_pessoa: str
    # Retorno: Objeto MongoClient
    def inserir_id_pessoa(self, id_ong, id_pessoa):
        return conn.adocao.ong.find_one_and_update({"_id": ObjectId(id_ong)}, {
            "$set": {
                "id_pessoa": id_pessoa
            }})

    # Objetivo: Encontrar uma ONG através do id e atualizar os campos com os atributos da classe
    # Parâmetros: id: str
    # Retorno:
    def atualizar_ong(self, id):
        conn.adocao.ong.find_one_and_update({"_id": ObjectId(id)}, {
            "$set": {
                "cnpj": self.cnpj,
                "nome": self.nome,
                "email": self.email,
                "telefone": self.telefone,
                "endereco": jsonable_encoder(self.endereco)
            }
        })

# Métodos estáticos
    @staticmethod
    # Objetivo: Retornar uma lista com todas as ONGs cadastradas
    # Parâmetros:
    # Retorno: Lista de dicionários contendo as ONGs cadastradas
    def retornar_ongs():
        return ongsEntity(conn.adocao.ong.find())

    @staticmethod
    # Objetivo: Encontrar a ONG que possua o id passado por parâmetro e retornar um dicionário com keys/values da ONG encontrada
    # Parâmetros: id: str
    # Retorno: Dicionário contendo keys/values da ONG cadastrada
    def retornar_uma_ong(id):
        return ongEntity(conn.adocao.ong.find_one({"_id": ObjectId(id)}))

    @staticmethod
    # Objetivo: Encontrar uma ONG pelo id e retornar um dicionário contendo key/value de nome da ONG
    # Parâmetros: id: str
    # Retorno: Dicionário contendo key/value do nome da ONG
    def retornar_nome_ong(id):
        return ongEntity(conn.adocao.ong.find_one(
            {"_id": ObjectId(id)}))["nome"]

    @staticmethod
    # Objetivo: Encontrar uma ONG através do id e retornar o id_pessoa
    # Parâmetros: id: str
    # Retorno: Dicionário com key/value do id_pessoa
    def retornar_id_pessoa(id):
        return ongEntity(conn.adocao.ong.find_one(
            {"_id": ObjectId(id)}))["id_pessoa"]

    @staticmethod
    # Objetivo: Encontrar a ONG que possua o id_pessoa passado por parâmetro e retornar o id_ong
    # Parâmetros: id_pessoa: str
    # Retorno: Dicionário contendo apenas key/value para id da ONG cadastrada
    def retornar_id_ong_por_pessoa(id_pessoa):
        return ongEntity(conn.adocao.ong.find_one(
            {"id_pessoa": id_pessoa}))["id"]

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
                id_pessoa = Ong.retornar_id_pessoa(id)
                emails.remove(
                    Ong.retornar_uma_pessoa(id_pessoa)["email"])
        return emails

    @staticmethod
    # Objetivo: Retornar uma lista contendo todos os CNPJs cadastrados
    # Parâmetros: id: str
    # Retorno: Lista de str contendo CNPJs
    def retornar_cnpjs_existentes(id=None):
        cnpjs = []
        if conn.adocao.ong.find().count() > 0:
            ongs = ongsEntity(conn.adocao.ong.find())
            for ong in ongs:
                cnpjs.append(ong["cnpj"])
            if id != None:
                cnpjs.remove(
                    Ong.retornar_uma_ong(id)["cnpj"])
        return cnpjs

    @staticmethod
    # Objetivo: Encontrar uma ONG através do id e deletar o cadastro
    # Parâmetros: id: str
    # Retorno:
    def deletar_ong(id):
        conn.adocao.ong.find_one_and_delete({"_id": ObjectId(id)})

# Exemplo de esquema

    class Config:
        schema_extra = {
            "example": {
                "cnpj": "65.705.048/0001-40",
                "nome": "Projeto Lontra",
                "email": "plontra@gmail.com.br",
                "telefone": "(51)94948-7887",
                "endereco": {
                    "cep": "93244-850",
                    "logradouro": "Av. das Missões",
                    "numero": 222,
                    "bairro": "Canoas",
                    "cidade": "Porto Alegre",
                    "estado": "RS"
                }
            }
        }
