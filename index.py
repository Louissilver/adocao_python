from fastapi import FastAPI
from routes.pet import pet
from routes.ong import ong
from routes.associado import associado
from routes.solicitacao_adocao import solicitacao_adocao
from routes.usuario import usuario
from routes.autenticacao import autenticacao

app = FastAPI()

app.include_router(pet)
app.include_router(ong)
app.include_router(associado)
app.include_router(solicitacao_adocao)
app.include_router(usuario)
app.include_router(autenticacao)
