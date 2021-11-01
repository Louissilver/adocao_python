from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from fastapi import status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.usuario import Usuario
from datetime import timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

autenticacao = APIRouter()


@autenticacao.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    login = form_data.username
    senha = form_data.password

    if Usuario.autenticar_usuario(login, senha):
        access_token = Usuario.criar_token_de_acesso(
            data={"sub": login}, expires_delta=timedelta(minutes=30))
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha incorretos.")


@autenticacao.get('/autenticacao', status_code=status.HTTP_200_OK)
async def autenticar(token: str = Depends(oauth2_scheme)):
    return {"token": token}
