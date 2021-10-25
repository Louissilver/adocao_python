from typing import Optional
from pydantic import BaseModel

from models.pessoa import Pessoa


class Ong(Pessoa):
    cnpj: str
    id_pessoa: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "cnpj": "65283608123",
                "nome": "Projeto Lontra",
                "email": "plontra@gmail.com.br",
                "telefone": "51949487887",
                "endereco": {
                    "cep": "93244850",
                    "logradouro": "Av. das Missões",
                    "numero": 222,
                    "bairro": "Canoas",
                    "cidade": "Porto Alegre",
                    "estado": "RS"
                }
            }
        }
