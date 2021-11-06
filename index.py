from fastapi import FastAPI
from routes.pet import pet
from routes.ong import ong
from routes.associado import associado
from routes.solicitacao_adocao import solicitacao_adocao
from routes.usuario import usuario
from routes.autenticacao import autenticacao
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:4000",
    "http://localhost:5000",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pet)
app.include_router(ong)
app.include_router(associado)
app.include_router(solicitacao_adocao)
app.include_router(usuario)
app.include_router(autenticacao)
