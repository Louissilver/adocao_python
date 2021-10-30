from fastapi.routing import APIRouter
from models.usuario import Usuario

usuario = APIRouter()


@usuario.get('/usuarios')
async def find_all_usuarios():
    return Usuario.retornar_usuarios()


@usuario.get('/usuarios/{id}')
async def find_one_usuario(id):
    return Usuario.retornar_um_usuario(id)


@usuario.put('/usuarios/{id}')
async def update_usuario(id, usuario: Usuario):
    usuario.atualizar_usuario(id)
    return f"A associado {usuario.login} foi alterado com sucesso!"
