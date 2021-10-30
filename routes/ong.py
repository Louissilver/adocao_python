from fastapi.routing import APIRouter
from models.ong import Ong
from models.pessoa import Pessoa
from models.usuario import Usuario

ong = APIRouter()


@ong.get('/ongs')
async def find_all_ongs():
    return Ong.retornar_ongs()


@ong.get('/ongs/{id}')
async def find_one_ong(id):
    return Ong.retornar_uma_ong(id)


@ong.post("/ongs")
async def create_ong(ong: Ong, usuario: Usuario):
    _id_pessoa = ong.inserir_pessoa()
    id_pessoa = str(_id_pessoa.inserted_id)

    _id_ong = ong.inserir_ong()
    id_ong = str(_id_ong.inserted_id)

    _id_usuario = usuario.inserir_usuario()
    id_usuario = str(_id_usuario.inserted_id)

    ong.inserir_id_pessoa(id_ong, id_pessoa)
    usuario.inserir_id_pessoa(id_usuario, id_pessoa)

    return f"ONG {ong.nome} inserida com sucesso!"


@ong.put('/ongs/{id}')
async def update_ong(id, ong: Ong):
    ong.atualizar_ong(id)
    return f"A ONG {ong.nome} foi alterada com sucesso!"


@ong.delete('/ongs/{id}')
async def delete_ong(id):
    ong = Ong.retornar_nome_ong(id)
    id_pessoa = Ong.retornar_id_pessoa(id)
    Usuario.deletar_usuario(id_pessoa)
    Pessoa.deletar_pessoa(id_pessoa)
    Ong.deletar_ong(id)
    return f"A ONG {ong} foi excluida com sucesso!"
