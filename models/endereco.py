import re
from fastapi import HTTPException, status
from pydantic import BaseModel
from pydantic import validator


class Endereco(BaseModel):
    cep: str
    logradouro: str
    numero: int
    bairro: str
    cidade: str
    estado: str

# Validadores
    @validator('cep')
    def validar_cep(cls, valor):
        valor = valor.strip()
        padrao = "^\d{5}-\d{3}$"
        validacao = re.match(padrao, valor)
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo CEP é obrigatório.")
        if not validacao:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O CEP informado não é válido. Tente o formato 'XXXXX-XXX'")
        return valor

    @validator('logradouro')
    def validar_logradouro(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo logradouro é obrigatório.")
        if len(valor) < 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O logradouro deve conter, pelo menos, 5 caracteres.")
        return valor

    @validator('numero')
    def validar_numero(cls, valor):
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo numero é obrigatório.")
        if valor <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O número não pode ser 0 ou negativo.")
        return valor

    @validator('bairro')
    def validar_bairro(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo bairro é obrigatório.")
        return valor

    @validator('cidade')
    def validar_cidade(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo cidade é obrigatório.")
        if len(valor) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="A cidade deve conter, pelo menos, 3 caracteres.")
        return valor

    @validator('estado')
    def validar_estado(cls, valor):
        valor = valor.strip()
        if valor == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O campo estado é obrigatório.")
        if len(valor) != 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="O estado informado não é válido. Tente novamente com formato em dois caracteres. Exemplo: RS, RJ, SP")
        return valor
