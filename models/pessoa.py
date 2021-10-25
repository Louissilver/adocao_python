from pydantic import BaseModel

from models.endereco import Endereco


class Pessoa(BaseModel):
    nome: str
    email: str
    telefone: str
    endereco: Endereco

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
