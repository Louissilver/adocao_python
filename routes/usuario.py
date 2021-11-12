from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from fastapi.security.oauth2 import OAuth2PasswordBearer
from models.associado import Associado
from models.usuario import Usuario
from models.ong import Ong
from fastapi import status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
usuario = APIRouter()


@usuario.get('/usuarios', status_code=status.HTTP_200_OK)
async def find_all_usuarios():
    return Usuario.retornar_usuarios()


@usuario.get('/usuarios/{id}', status_code=status.HTTP_200_OK)
async def find_one_usuario(id):
    return Usuario.retornar_um_usuario(id)


@usuario.get('/usuarios/existe/{login}', status_code=status.HTTP_200_OK)
async def find_usuario_por_login(login):
    return Usuario.retornar_usuario_por_login(login)


@usuario.put('/usuarios/{id}', status_code=status.HTTP_200_OK)
async def update_usuario(id, usuario: Usuario):
    if usuario.login in Usuario.retornar_logins_existentes(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="O login informado já está em uso.")
    usuario.senha = Usuario.get_passwordhash(usuario.senha)
    usuario.atualizar_usuario(id)
    return f"O usuário {usuario.login} foi alterado com sucesso!"


@usuario.get('/usuario/atual', status_code=status.HTTP_200_OK)
async def autenticar(token: str):
    usuario_atual = Usuario.retornar_usuario_atual(token)
    [tipo_usuario, id_pessoa] = Usuario.retornar_tipo_usuario(usuario_atual)
    if(tipo_usuario == "ONG"):
        id_tipo_pessoa = Ong.retornar_id_ong_por_pessoa(id_pessoa)
    if(tipo_usuario == "Associado"):
        id_tipo_pessoa = Associado.retornar_id_associado_por_pessoa(id_pessoa)
    return {"token": token, "usuario_atual": usuario_atual, "tipo_usuario": tipo_usuario, "id_tipo_pessoa": id_tipo_pessoa}
