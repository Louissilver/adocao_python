from typing import Optional
from bson import ObjectId
from fastapi import HTTPException, status
from pydantic import BaseModel
from datetime import datetime
from pydantic import validator
from config.db import conn
from models.associado import Associado
from models.pet import Pet
from email_validator import EmailNotValidError, validate_email
from schemas.solicitacao_adocao import solicitacao_adocaoEntity, solicitacoes_adocaoEntity
import re


class Solicitacao_Adocao(BaseModel):
    id_associado: str
    id_ong: str
    id_pet: str
    nome_pet: str
    nome_ong: str
    cnpj_ong: str
    telefone_ong: str
    email_ong: str
    nome_associado: str
    cpf_associado: str
    telefone_associado: str
    email_associado: str
    aprovado: Optional[bool]
    finalizado: Optional[bool]
    referencias: str
    dataSolicitacao: Optional[datetime]

    @validator('nome_pet')
    def validar_nome(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo nome é obrigatório.")
        if len(valor) <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O nome deve conter, pelo menos, 2 caracteres.")
        return valor

    @validator('nome_ong')
    def validar_nome_ong(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo nome é obrigatório.")
        if len(valor) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O nome deve conter, pelo menos, 3 caracteres.")
        return valor

    @validator('nome_associado')
    def validar_nome_associado(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo nome é obrigatório.")
        if len(valor) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O nome deve conter, pelo menos, 3 caracteres.")
        return valor

    @validator('cpf_associado')
    def validar_cpf(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo CPF é obrigatório.")
        padrao = "^\d{3}\.\d{3}\.\d{3}\-\d{2}$"
        validacao = re.match(padrao, valor)
        if not validacao:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O CPF informado não é válido. Tente o formato 'XXX.XXX.XXX-XX'")
        return valor

    @validator('cnpj_ong')
    def validar_cnpj(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo CNPJ é obrigatório.")
        padrao = "^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$"
        validacao = re.match(padrao, valor)
        if not validacao:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O CNPJ informado não é válido. Tente o formato 'XX.XXX.XXX/XXXX-XX'")
        return valor

    @validator('id_associado')
    def validar_id_associado(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo id_associado é obrigatório.")
        return valor

    @validator('id_ong')
    def validar_id_ong(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo id_ong é obrigatório.")
        return valor

    @validator('id_pet')
    def validar_id_pet(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo id_pet é obrigatório.")
        return valor

    @validator('referencias')
    def validar_referencias(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo referencias é obrigatório.")
        if len(valor) < 30 or (' ' not in valor):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="As referências informadas devem conter, pelo menos, 30 caracteres e espaços, formando um texto.")
        return valor

    @validator('email_ong', pre=True)
    def validar_email_ong(cls, valor):
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

    @validator('telefone_ong', pre=True)
    def validar_telefone_ong(cls, valor):
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

    @validator('email_associado', pre=True)
    def validar_email_associado(cls, valor):
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

    @validator('telefone_associado', pre=True)
    def validar_telefone_associado(cls, valor):
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

    @staticmethod
    def retornar_solicitacoes():
        return solicitacoes_adocaoEntity(conn.adocao.solicitacao_adocao.find())

    @staticmethod
    def retornar_uma_solicitacao(id):
        return solicitacao_adocaoEntity(conn.adocao.solicitacao_adocao.find_one({"_id": ObjectId(id)}))

    def inserir_solicitacao(self):
        return conn.adocao.solicitacao_adocao.insert_one({
            "id_associado": self.id_associado,
            "id_ong": self.id_ong,
            "id_pet": self.id_pet,
            "nome_pet": self.nome_pet,
            "nome_ong": self.nome_ong,
            "cnpj_ong": self.cnpj_ong,
            "telefone_ong": self.telefone_ong,
            "email_ong": self.email_ong,
            "nome_associado": self.nome_associado,
            "cpf_associado": self.cpf_associado,
            "telefone_associado": self.telefone_associado,
            "email_associado": self.email_associado,
            "aprovado": False,
            "finalizado": False,
            "referencias": self.referencias,
            "dataSolicitacao": datetime.now(),
        })

    def atualizar_solicitacao(self, id):
        conn.adocao.solicitacao_adocao.find_one_and_update({"_id": ObjectId(id)}, {
            "$set": {
                "id_associado": self.id_associado,
                "id_ong": self.id_ong,
                "id_pet": self.id_pet,
                "nome_pet": self.nome_pet,
                "nome_ong": self.nome_ong,
                "cnpj_ong": self.cnpj_ong,
                "telefone_ong": self.telefone_ong,
                "email_ong": self.email_ong,
                "nome_associado": self.nome_associado,
                "cpf_associado": self.cpf_associado,
                "telefone_associado": self.telefone_associado,
                "email_associado": self.email_associado,
                "referencias": self.referencias,
            }
        })

    @staticmethod
    def aprovar_solicitacao(id):
        solicitacao = Solicitacao_Adocao.retornar_uma_solicitacao(id)
        if solicitacao["aprovado"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="A solicitação já foi aprovada")
        conn.adocao.solicitacao_adocao.find_one_and_update({"_id": ObjectId(id)}, {
            "$set": {
                "aprovado": True
            }
        })
        return Solicitacao_Adocao.retornar_id_solicitacao(id)

    @staticmethod
    def finalizar_solicitacao(id):
        solicitacao = Solicitacao_Adocao.retornar_uma_solicitacao(id)
        if solicitacao["finalizado"] == True:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="A solicitação já foi finalizada")
        if solicitacao["aprovado"]:
            Associado.incluir_pet(solicitacao)
            Pet.ser_adotado(solicitacao)
        conn.adocao.solicitacao_adocao.find_one_and_update({"_id": ObjectId(id)}, {
            "$set": {
                "finalizado": True
            }
        })
        return Solicitacao_Adocao.retornar_id_solicitacao(id)

    @staticmethod
    def retornar_id_solicitacao(id):
        return solicitacao_adocaoEntity(conn.adocao.solicitacao_adocao.find_one({"_id": ObjectId(id)}))["id"]

    @staticmethod
    def deletar_solicitacao(id):
        conn.adocao.solicitacao_adocao.find_one_and_delete(
            {"_id": ObjectId(id)})

    class Config:
        schema_extra = {
            "example": {
                "id_associado": "6171db8444806f2e8000bf42",
                "id_ong": "6171db6244806f2e8000bf41",
                "id_pet": "6171dbb644806f2e8000bf45",
                "nome_pet": "Rubídio",
                "nome_ong": "Anjos de Rua",
                "cnpj_ong": "65.705.048/0001-40",
                "telefone_ong": "(51)3344-5515",
                "email_ong": "anjr@example.com",
                "nome_associado": "Luís Fernando da Silveira",
                "cpf_associado": "453.964.972-89",
                "telefone_associado": "(51)99344-5515",
                "email_associado": "luisfsilveira@example.com",
                "referencias": "Tenho um filho que ama animais, um pátio enorme e atualmente já cuido ...",
            }
        }
