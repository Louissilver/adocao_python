from fastapi.param_functions import Body, Depends
from fastapi.routing import APIRouter
from fastapi import status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.usuario import Usuario
from datetime import timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

autenticacao = APIRouter()


@autenticacao.post("/token")
def gerar_token(login: str = Body(...), senha: str = Body(...)):
    if Usuario.autenticar_usuario(login, senha):
        access_token = Usuario.criar_token_de_acesso(
            data={"sub": login}, expires_delta=timedelta(minutes=30))
        tipo_usuario = Usuario.retornar_tipo_usuario(login)
        return {"access_token": access_token, "token_type": "bearer", "tipo_usuario": tipo_usuario}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha incorretos.")
