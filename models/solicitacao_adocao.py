from pydantic import BaseModel
from datetime import datetime


class Solicitacao_Adocao(BaseModel):
    id_associado: str
    id_ong: str
    id_pet: str
    aprovado: bool
    finalizado: bool
    referencias: str
    dataSolicitacao: datetime

    class Config:
        schema_extra = {
            "example": {
                "id_associado": "6171db8444806f2e8000bf42",
                "id_ong": "6171db6244806f2e8000bf41",
                "id_pet": "6171dbb644806f2e8000bf45",
                "aprovado": False,
                "finalizado": False,
                "referencias": "Tenho um filho que ama animais, um pátio enorme e atualmente já cuido ...",
                "dataSolicitacao": datetime.now(),
            }
        }
