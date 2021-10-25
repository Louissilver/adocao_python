from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from models.pessoa import Pessoa


class Associado(Pessoa):
    cpf: str
    dataNascimento: datetime
    animaisAdotados: Optional[List[str]]
    id_pessoa: Optional[str]

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
                },
                "cpf": "45396497289",
                "dataNascimento": datetime(1999, 3, 19),
                "animaisAdotados": [],
            }
        }
