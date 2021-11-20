import re
from typing import List, Optional
from datetime import datetime
from pydantic import validator
from bson import ObjectId
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from schemas.associado import associadoEntity, associadosEntity
from config.db import conn
from models.pessoa import Pessoa
from schemas.pessoa import pessoasEntity
from helpers.dataHelper import retornar_data


class Associado(Pessoa):
    cpf: str
    dataNascimento: str
    animaisAdotados: Optional[List[str]]
    id_pessoa: Optional[str]

# Validadores
    @validator('cpf')
    def validar_cpf(cls, valor):
        valor = valor.strip()
        padrao = "^\d{3}\.\d{3}\.\d{3}\-\d{2}$"
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo CPF é obrigatório.")
        validacao = re.match(padrao, valor)
        if not validacao:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O CPF informado não é válido. Tente o formato 'XXX.XXX.XXX-XX'")
        return valor

    @validator('dataNascimento')
    def validar_dataNascimento(cls, valor):
        valor = valor.strip()
        padrao = "^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$"
        dia, mes, ano = retornar_data(valor)
        validacao = re.match(padrao, valor)
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo dataNascimento é obrigatório.")
        if not validacao:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="A data informada não é válida. Tente o formato 'dd/mm/yyyy'")
        if datetime(ano + 18, mes, dia) >= datetime.now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="A idade para cadastro deve ser maior que 18 anos.")
        return valor

# Métodos de instância

    # Objetivo: Encontrar um associado através do id e atualizar os campos com os atributos da classe
    # Parâmetros: id: str
    # Retorno:
    def atualizar_associado(self, id):
        dia, mes, ano = retornar_data(self.dataNascimento)
        conn.adocao.associado.find_one_and_update({"_id": ObjectId(id)}, {
            "$set": {
                "nome": self.nome,
                "email": self.email,
                "telefone": self.telefone,
                "endereco": jsonable_encoder(self.endereco),
                "cpf": self.cpf,
                "dataNascimento": datetime(ano, mes, dia),
                "animaisAdotados": self.animaisAdotados,
            }
        })

    # Objetivo: Inserir no banco um registro de associado utilizando os atributos da classe
    # Parâmetros:
    # Retorno: Objeto MongoClient
    def inserir_associado(self):
        dia, mes, ano = retornar_data(self.dataNascimento)
        return conn.adocao.associado.insert_one({
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "endereco": jsonable_encoder(self.endereco),
            "cpf": self.cpf,
            "dataNascimento": datetime(ano, mes, dia),
            "animaisAdotados": self.animaisAdotados,
        })

    # Objetivo: Encontrar um associado através do id_associado e incluir o id_pessoa
    # Parâmetros: id_associado: str, id_pessoa: str
    # Retorno: Objeto MongoClient
    def inserir_id_pessoa(self, id_associado, id_pessoa):
        return conn.adocao.associado.find_one_and_update({"_id": ObjectId(id_associado)}, {
            "$set": {
                "id_pessoa": id_pessoa
            }})

# Métodos Estáticos
    @staticmethod
    # Objetivo: Retornar uma lista com todos os associados cadastrados
    # Parâmetros:
    # Retorno: Lista de dicionários contendo os associados cadastrados
    def retornar_associados():
        return associadosEntity(conn.adocao.associado.find())

    @staticmethod
    # Objetivo: Encontrar o associado que possua o id passado por parâmetro e retornar um dicionário com keys/values do associado encontrado
    # Parâmetros: id: str
    # Retorno: Dicionário contendo keys/values do associado cadastrado
    def retornar_um_associado(id):
        ids = []
        for i in Associado.retornar_associados():
            ids.append(i["id"])
        if id not in ids:
            raise HTTPException(
                status_code=404, detail="Não foi possível encontrar nenhum associado com esse id.")
        return associadoEntity(conn.adocao.associado.find_one({"_id": ObjectId(id)}))

    @staticmethod
    # Objetivo: Encontrar um associado através do id e deletar o cadastro
    # Parâmetros: id: str
    # Retorno:
    def deletar_associado(id):
        conn.adocao.associado.find_one_and_delete(
            {"_id": ObjectId(id)})

    @staticmethod
    # Objetivo: Encontrar um associado pelo id e retornar um dicionário contendo key/value de nome do associado
    # Parâmetros: id: str
    # Retorno: Dicionário contendo key/value do nome do associado
    def retornar_nome_associado(id):
        return associadoEntity(conn.adocao.associado.find_one({"_id": ObjectId(id)}))["nome"]

    @staticmethod
    # Objetivo: Encontrar o associado que possua o id_pessoa passado por parâmetro e retornar o id de associado
    # Parâmetros: id_pessoa: str
    # Retorno: Dicionário contendo apenas key/value para id do associado cadastrado
    def retornar_id_associado_por_pessoa(id_pessoa):
        return associadoEntity(conn.adocao.associado.find_one(
            {"id_pessoa": id_pessoa}))["id"]

    @staticmethod
    # Objetivo: Encontrar o associado por id_associado e incluir o id_pet no array de animaisAdotados
    # Parâmetros: solicitacao: Solicitacao
    # Retorno:
    def incluir_pet(solicitacao):
        conn.adocao.associado.find_one_and_update({"_id": ObjectId(solicitacao["id_associado"])}, {
            "$push": {"animaisAdotados": solicitacao["id_pet"]}})

    @staticmethod
    # Objetivo: Encontrar um associado através do id e retornar o id_pessoa
    # Parâmetros: id: str
    # Retorno: Dicionário com key/value do id_pessoa
    def retornar_id_pessoa(id):
        return associadoEntity(conn.adocao.associado.find_one(
            {"_id": ObjectId(id)}))["id_pessoa"]

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
                id_pessoa = Associado.retornar_id_pessoa(id)
                emails.remove(
                    Associado.retornar_uma_pessoa(id_pessoa)["email"])
        return emails

    @staticmethod
    # Objetivo: Retornar uma lista contendo todos os CPFs cadastrados
    # Parâmetros: id: str
    # Retorno: Lista de str contendo CPFs
    def retornar_cpfs_existentes(id=None):
        cpfs = []
        if conn.adocao.associado.find().count() > 0:
            associados = associadosEntity(conn.adocao.associado.find())
            for associado in associados:
                cpfs.append(associado["cpf"])
            if id != None:
                cpfs.remove(
                    Associado.retornar_um_associado(id)["cpf"])
        return cpfs

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
                },
                "cpf": "453.964.972-89",
                "dataNascimento": "19/03/2019",
                "animaisAdotados": [],
            }
        }
