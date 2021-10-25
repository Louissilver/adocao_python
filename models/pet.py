from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Pet(BaseModel):
    nome: str
    especie: str
    raca: str
    dataNascimento: datetime
    sexo: str
    porte: str
    adotado: bool
    urlFoto: str
    observacoes: str
    id_ong: Optional[str]
    id_associado: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "nome": "Rubídio",
                "especie": "Cachorro",
                "raca": "SRD",
                "dataNascimento": datetime(2018, 3, 26),
                "sexo": "M",
                "porte": "Médio",
                "adotado": False,
                "urlFoto": "https://4.bp.blogspot.com/_gWqerMk_ui0/Rvq7ZbayoEI/AAAAAAAAA8Q/xU696jlpw68/s320/Rabbit.jpg",
                "observacoes": "Cãozinho muito dócil, brincalhão, companheiro. Adora dormir com a cabeça no travesseiro",
            }
        }
