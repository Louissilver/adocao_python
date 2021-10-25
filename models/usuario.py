from typing import Optional
from pydantic import BaseModel


class Usuario(BaseModel):
    login: str
    senha: str
    tipo_usuario: str
    id_pessoa: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "login": "ondaanimal@gmail.com",
                "senha": "12345",
                "tipo_usuario": "ONG",
            }
        }
