from fastapi.routing import APIRouter
from models.usuario import Usuario
from fastapi import status

usuario = APIRouter()


@usuario.get('/usuarios', status_code=status.HTTP_200_OK)
async def find_all_usuarios():
    return Usuario.retornar_usuarios()


@usuario.get('/usuarios/{id}', status_code=status.HTTP_200_OK)
async def find_one_usuario(id):
    return Usuario.retornar_um_usuario(id)


@usuario.put('/usuarios/{id}', status_code=status.HTTP_200_OK)
async def update_usuario(id, usuario: Usuario):
    usuario.atualizar_usuario(id)
    return f"O usuário {usuario.login} foi alterado com sucesso!"
