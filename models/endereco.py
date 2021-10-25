from bson import ObjectId
from pydantic import BaseModel


class Endereco(BaseModel):
    cep: str
    logradouro: str
    numero: int
    bairro: str
    cidade: str
    estado: str
