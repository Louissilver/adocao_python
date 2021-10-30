from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from config.db import conn
from models.endereco import Endereco
from schemas.pessoa import pessoaEntity


class Pessoa(BaseModel):
    nome: str
    email: str
    telefone: str
    endereco: Endereco

    def inserir_pessoa(self):
        return conn.local.pessoa.insert_one({
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "endereco": jsonable_encoder(self.endereco)
        })

    @staticmethod
    def deletar_pessoa(id_pessoa):
        conn.local.pessoa.find_one_and_delete({"_id": ObjectId(id_pessoa)})

    class Config:
        schema_extra = {
            "example": {
                "nome": "Luís Fernando da Silveira",
                "email": "luis.202020718@unilasalle.edu.br",
                "telefone": "51995814416",
                "endereco": {
                    "cep": "93600000",
                    "logradouro": "Av. das Rosas",
                    "numero": 1410,
                    "bairro": "Floresta",
                    "cidade": "Estância Velha",
                    "estado": "RS"
                }
            }
        }
